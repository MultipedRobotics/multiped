from math import acos, pi
import numpy as np

rad2deg = 180/pi
deg2rad = pi/180

def constrain(angle, min, max):
    angle = angle if angle > min else min
    angle = angle if angle < max else max
    return angle

def cosinelaw(a,b,c):
    # cos(g) = (a^2+b^2-c^2)/2ab
    return acos((a**2+b**2-c**2)/(2*a*b))

def Rz(a, degrees=False):
    if degrees:
        a *= deg2rad
    ca = np.cos(a)
    sa = np.sin(a)
    return np.array(
        [[ ca, sa, 0],
         [-sa, ca, 0],
         [  0,  0, 1]]
    )
