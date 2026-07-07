# AGV Emergency Stop: Multi-Layer Formal Verification

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![IEEE Access](https://img.shields.io/badge/Published-IEEE%20Access%202026-blue)](https://ieeeaccess.ieee.org/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)

Supplementary materials for the paper:

> **From Normative Text to Verified Control Logic: Multi-Layer Formal Verification and Hardware-in-the-Loop Validation of AGV Emergency Stop Logic**
>
> Michal Skupny, Joanna Piasek-Skupna  
> Poznan University of Technology, Poland

## Overview

This repository contains a complete four-layer verification pipeline for safety-critical control systems:

1. **Layer 1 (FRET)**: Normative consistency analysis
2. **Layer 2 (NuSMV)**: Behavioral model checking → discovers 1-cycle permissive window
3. **Layer 3 (UPPAAL)**: Time-bounded verification with atomic updates
4. **Layer 4 (HIL)**: Hardware validation on Siemens S7-1200 (200 automated trials)

### Key Finding

Original design exhibits 1-scan (10 ms) motion latency after e-stop. Fixed design (REQ-7) achieves 0-scan latency. Deterministic behavior across all 200 hardware trials (σ=0.0).

## Repository Structure

```
agv-estop-verification/
├── paper/                    # Published article + figures
├── models/                   # FRET, NuSMV, UPPAAL models
├── controllers/              # IEC 61131-3 control logic
├── hil/                      # Hardware test results & harness
├── oracle/                   # SIL Oracle simulation
└── docs/                     # Reproducibility guides
```

## Quick Start

**View paper:**
```bash
open paper/skupny_ieee_access.pdf
```

**Verify NuSMV model:**
```bash
nusmv models/nusmv/estop_fixed.smv
```

**Check HIL results:**
```bash
cat hil/results/hil_analysis.txt
```

## Hardware-in-the-Loop Testing

- **Hardware**: Siemens S7-1200 (CPU 1212C)
- **Cycle Time**: 10 ms
- **Trials**: 200 automated
- **Result**: Variant A = 1 scan, Variant B = 0 scans (deterministic)

## Requirements

- **FRET** v3.0
- **NuSMV** v2.6.0+
- **UPPAAL** v4.1.26+
- **Python** 3.8+

## How to Cite

```bibtex
@article{skupny2026verification,
  title={From Normative Text to Verified Control Logic: Multi-Layer Formal 
         Verification and Hardware-in-the-Loop Validation of AGV Emergency Stop Logic},
  author={Skupny, Michal},
  journal={},
  year={2026}
}
```

## License

CC-BY-4.0 (Creative Commons Attribution 4.0 International)

## Authors

- **Michal Skupny** — Poznan University of Technology
- **Joanna Piasek-Skupna** — Poznan University of Technology

---

For detailed reproduction instructions, see [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md).
