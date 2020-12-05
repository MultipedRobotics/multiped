#############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

# import numpy as np
from math import sin, cos, acos, atan2, sqrt, pi, fabs
# from math import radians as d2r
# from math import degrees as r2d
from .utils import constrain
from .utils import cosinelaw
from .utils import rad2deg, deg2rad

# def sq(x):
#     return x*x

class Leg3:
    """
    parameter file:
    {
        "legs": {
            0: {
                "linkLengths": [coxa, femur, tibia], # mm
                "servoOffsets": [s0, s1, s2],        # radians
                "servoLimits": [(min,max), (min,max), (min, max)] # radians
                "ids": [4,5,6] # servo ID numbers
            }
        }
    }
    """
    def __init__(self, params):
        self.linkLengths = params["linkLengths"]
        self.servoOffsets = list(deg2rad*x for x in params["servoOffsets"])
        self.servoLimits = list((deg2rad*a, deg2rad*b) for a,b in params["servoLimits"])
        self.ids = params["ids"]

    def forward(self, t1,t2,t3, deg=True):
        """
        Forward kinematics of the leg where angles a,b,c can be degrees [default]
        or radians. Output is in the same units as the link lengths.
        """
        l1,l2,l3 = self.linkLengths

        if degrees:
            t1 *= deg2rad
            t2 *= deg2rad
            t3 *= deg2rad

        x = (l1 + l2*cos(t2) + l3*cos(t2 + t3))*cos(t1)
        y = (l1 + l2*cos(t2) + l3*cos(t2 + t3))*sin(t1)
        z = l2*sin(t2) + l3*sin(t2 + t3)
        return (x,y,z)

    def inverse(self, x,y,z, degrees=False):
        """
        Given a point in 3D space (x,y,z), this returns the joint angles in
        radians [default] or degrees as a tuple (theta1, theta2, theta3).
        """
        # mm
        l1,l2,l3 = self.linkLengths

        w = sqrt(x**2+y**2) - l1
        d = sqrt(w**2+z**2)

        t1 = atan2(y,x)
        t2 = atan2(z,w)+cosinelaw(l2,d,l3)
        t3 = cosinelaw(l2,l3,d)-pi

        if degrees:
            t1 *= rad2deg
            t2 *= rad2deg
            t3 *= rad2deg

        return (t1,t2,t3)
