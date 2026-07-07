Input	
	e_stop:	Bool
	reset:	Bool
	start:	Bool
Output	
	perm:	Bool
	motion:	Bool
Static	
	perm_state:	Bool
	perm_prev:	Bool
	motion_state:	Bool

	

BEGIN_BLOCK
IF #e_stop= FALSE THEN
    #perm_state := FALSE;
ELSIF #reset = TRUE THEN
    #perm_state := TRUE;
END_IF;
IF (#perm_prev = TRUE AND #start = TRUE) THEN
    #motion_state:= TRUE;
ELSIF #perm_prev = FALSE THEN
    #motion_state := FALSE;
END_IF;
IF #perm_state = TRUE THEN
    #perm := TRUE;
ELSE
    #perm := FALSE;
END_IF;
#perm_prev := #perm_state;
#motion := #motion_state;
END_BLOCK
