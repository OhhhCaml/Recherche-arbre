from math import *

def force_to_temps(F_vent):
    return(0.1*(pi/2 + atan(1-0.1*F_vent)))
