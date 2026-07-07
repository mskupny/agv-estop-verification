#!/usr/bin/env python3
"""
Reference software-in-the-loop simulation for the AGV e-stop one-cycle gap.

This is the OFFLINE ORACLE: it executes the SAME scan-cycle controller logic
as estop_naive.st / estop_fixed.st against a differential-drive kinematic
plant, and reproduces the one-cycle motion overrun + the REQ-7 fix.

IMPORTANT FOR THE PAPER:
  SCAN_TIME_S below is a REPRESENTATIVE placeholder. The paper's measured
  number must come from the real OpenPLC run (openplc_sil_harness.py records
  it). This sim shows the *phenomenon and the geometry*; OpenPLC supplies the
  *measured* scan time that scales the travel figure.
"""
import numpy as np
import matplotlib.pyplot as plt
import os

SCAN_TIME_S = 0.010      # placeholder; REPLACE with measured OpenPLC scan time
V_NOMINAL   = 1.5        # m/s, mid-range AGV speed (paper: 1-2 m/s)

# ---------------- controllers (mirror the ST exactly) ----------------
def controller_naive(inp, st):
    estop, reset, start = inp["estop"], inp["reset"], inp["start"]
    # motion reads PREVIOUS scan's permission -> the gap
    if st["perm_prev"] and start:
        st["run"] = True
    elif not st["perm_prev"]:
        st["run"] = False
    # permission updates this scan
    if not estop:
        st["perm"] = False
    elif reset:
        st["perm"] = True
    st["auto"] = st["perm"]; st["hand"] = st["perm"]
    st["perm_prev"] = st["perm"]
    return st

def controller_fixed(inp, st):
    estop, reset, start = inp["estop"], inp["reset"], inp["start"]
    if not estop:
        st["perm"] = False
    elif reset:
        st["perm"] = True
    st["auto"] = st["perm"]; st["hand"] = st["perm"]
    if st["perm_prev"] and start:
        st["run"] = True
    elif not st["perm_prev"]:
        st["run"] = False
    if not estop:                 # REQ-7 same-scan override
        st["run"] = False
    st["perm_prev"] = st["perm"]
    return st

# ---------------- differential-drive plant (linear travel) ----------------
def run_scenario(controller):
    st = dict(perm=False, perm_prev=False, run=False, auto=False, hand=False)
    N = 40
    estop_press = 20             # cycle at which operator hits e-stop
    pos = 0.0
    log = []
    for k in range(N):
        # operator inputs (active-low estop: True = released/ok)
        estop = (k < estop_press)              # pressed from cycle 20 on
        reset = (k == 2)                       # reset early
        start = (k >= 4)                       # start command held
        st = controller(dict(estop=estop, reset=reset, start=start), st)
        v = V_NOMINAL if st["run"] else 0.0    # drives move only if running
        pos += v * SCAN_TIME_S
        log.append((k, st["perm"], st["run"], pos))
    return np.array(log, dtype=float), estop_press

naive, tp = run_scenario(controller_naive)
fixed, _  = run_scenario(controller_fixed)

# overrun = scans where run==True after e-stop pressed (k>=tp)
def overrun_metrics(log, tp):
    mask = (log[:,0] >= tp) & (log[:,2] == 1.0)
    n_over = int(mask.sum())
    travel = n_over * V_NOMINAL * SCAN_TIME_S
    return n_over, travel

n_n, d_n = overrun_metrics(naive, tp)
n_f, d_f = overrun_metrics(fixed, tp)

print("====== AGV E-STOP MOTION OVERRUN ORACLE ======")
print(f"SCAN_TIME_S (placeholder) = {SCAN_TIME_S*1000:.1f} ms,  v = {V_NOMINAL} m/s")
print(f"NAIVE : overrun scans after e-stop = {n_n}, extra travel = {d_n*1000:.1f} mm")
print(f"FIXED : overrun scans after e-stop = {n_f}, extra travel = {d_f*1000:.1f} mm")

# ---------------- figure ----------------
fig, axes = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
for ax, log, title, n_over in [
        (axes[0], naive, "Naive (motion gated through permission state)", n_n),
        (axes[1], fixed, "REQ-7 (direct e-stop → motion inhibit)",   n_f)]:
    k = log[:,0]
    ax.step(k, log[:,1], where="post", label="eStopPermissionOk", lw=2)
    ax.step(k, log[:,2]-1.15, where="post", label="continueRunning", lw=2)
    ax.axvline(tp, color="r", ls="--", lw=1, alpha=.7)
    ax.text(tp+0.2, 1.05, "e-stop pressed", color="r", fontsize=9)
    if n_over:
        ax.axvspan(tp, tp+n_over, color="r", alpha=.12)
        ax.text(tp+0.2, -1.4, f"{n_over}-scan overrun", color="r", fontsize=9)
    ax.set_yticks([1, -0.15]); ax.set_yticklabels(["perm", "run"])
    ax.set_ylim(-1.7, 1.6); ax.set_title(title, fontsize=10)
    ax.legend(loc="upper right", fontsize=8); ax.grid(alpha=.25)
axes[1].set_xlabel("PLC scan cycle k")
fig.suptitle("AGV e-stop: one-cycle motion overrun and its REQ-7 elimination",
             fontsize=12, y=0.99)
fig.tight_layout(rect=[0,0,1,0.97])

# FIXED: Use current directory if folder doesn't exist
output_path = "overrun_figure.png"
try:
    output_path = os.path.join(os.getcwd(), "overrun_figure.png")
    fig.savefig(output_path, dpi=150)
    print(f"figure -> {output_path}")
except:
    output_path = "overrun_figure.png"

fig.savefig(output_path, dpi=150)
print(f"figure -> {output_path}")
print("Done")
