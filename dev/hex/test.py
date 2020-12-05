#!/usr/bin/env python3

from multiped.gait import TripodGait
from multiped.engine import Engine
from pyservos.ax12 import AX12

t = TripodGait()
# ans = t.command(1,0,0,0)

# print(ans)

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
params = {
    "legs": {
        0: {
            "linkLengths": [50, 65, 68],               # mm
            "servoOffsets": [0, 0, 0],                   # deg
            "servoLimits": [(0,300), (0,300), (0, 300)], # deg
            "ids": [1,2,3] # servo ID numbers
        },
        1: {
            "linkLengths": [50, 65, 68],               # mm
            "servoOffsets": [0, 0, 0],                   # deg
            "servoLimits": [(0,300), (0,300), (0, 300)], # deg
            "ids": [4,5,6] # servo ID numbers
        },
        2: {
            "linkLengths": [50, 65, 68],               # mm
            "servoOffsets": [0, 0, 0],                   # deg
            "servoLimits": [(0,300), (0,300), (0, 300)], # deg
            "ids": [7,8,9] # servo ID numbers
        },
        3: {
            "linkLengths": [50, 65, 68],               # mm
            "servoOffsets": [0, 0, 0],                   # deg
            "servoLimits": [(0,300), (0,300), (0, 300)], # deg
            "ids": [10,11,12] # servo ID numbers
        },
        4: {
            "linkLengths": [50, 65, 68],               # mm
            "servoOffsets": [0, 0, 0],                   # deg
            "servoLimits": [(0,300), (0,300), (0, 300)], # deg
            "ids": [13,14,15] # servo ID numbers
        },
        5: {
            "linkLengths": [50, 65, 68],               # mm
            "servoOffsets": [0, 0, 0],                   # deg
            "servoLimits": [(0,300), (0,300), (0, 300)], # deg
            "ids": [16,17,18] # servo ID numbers
        },
    }
}

# e = Engine(params, None, AX12)
# e.setGait(TripodGait)
# e.move(1,0,0,0)
