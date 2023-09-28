# Define scale factors [WT]
def get_scale_factor(unit):
    BARN_CM2= 1e-24
    
    if (unit == "b"):
        return BARN_CM
    elif (unit == "mb"):
        return 1e-3*BARN_CM2
    elif (unit == "ub"):
        return 1e-6*BARN_CM2
    elif (unit == "nb"):
        return 1e-9*BARN_CM2
    elif (unit == "pb"):
        return 1e-12*BARN_CM2
    elif (unit == "fb"):
        return 1e-15*BARN_CM2
    elif (unit == "ab"):
        return 1e-18*BARN_CM2
    elif (unit == "zb"):
        return 1e-21*BARN_CM2
    elif (unit == "yb"):
        return 1e-24*BARN_CM2
    else: 
        return 1