##############################################
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























#
# from __future__ import print_function
# from __future__ import division
# # import numpy as np
# from math import sin, cos, acos, atan2, sqrt, pi, fabs
# from math import radians as d2r
# from math import degrees as r2d
# # import logging
# from .Servo import Servo
#
# # logging.basicConfig(level=logging.DEBUG)
# # logging.basicConfig(level=logging.ERROR)
#
#
# class LegException(Exception):
#     pass
#
#
# class Leg3(object):
#     """
#     """
#     # these are fixed by the 3D printing, not changing
#     coxaLength = 45.0
#     tibiaLength = 55.0
#     femurLength = 104.0
#     s_limits = [
#         [-90, 90],  # set limits
#         [-90, 90],
#         [-150, 0]
#     ]
#     s_offsets = [150, 150, 150+90]  # angle offsets to line up with fk
#
#     sit_raw = (150, 270, 100)
#     stand_raw = (150, 175, 172)
#     sit_angles = None
#     stand_angles = None
#
#     def __init__(self, channels):
#         """
#         Each leg has 3 servos/channels
#         """
#         if not len(channels) == 3:
#             raise LegException('len(channels) != 3')
#
#         Servo.bulkServoWrite = True
#
#         # angle offsets to line up with fk
#         self.servos = []
#         for i in range(0, 3):
#             self.servos.append(Servo(channels[i]))
#             self.servos[i].setServoLimits(self.s_offsets[i], *self.s_limits[i])
#
#         self.sit_angles = self.convertRawAngles(*self.sit_raw)
#         initAngles = self.convertRawAngles(*self.stand_raw)
#         self.stand_angles = initAngles
#         self.foot0 = self.fk(*initAngles)  # rest/idle position of the foot/leg
#
#     def __del__(self):
#         pass
#
#     def sit(self):
#         self.moveFootAngles(*self.sit_angles)
#
#     def stand(self):
#         self.moveFootAngles(*self.stand_angles)
#
#     def convertRawAngles(self, a, b, c):
#         return (a-self.s_offsets[0], b-self.s_offsets[1], c-self.s_offsets[2])
#
#     def fk(self, a, b, g):
#         """
#         Forward kinematics of the leg, note, angle are all degrees
#         """
#         Lc = self.coxaLength
#         Lf = self.femurLength
#         Lt = self.tibiaLength
#
#         a = d2r(a)
#         b = d2r(b)
#         g = d2r(g)
#
#         foot = [
#             (Lc + Lf*cos(b) + Lt*cos(b + g))*cos(a),
#             (Lc + Lf*cos(b) + Lt*cos(b + g))*sin(a),
#             Lf*sin(b) + Lt*sin(b + g)
#         ]
#
#         # return np.array(foot)
#         return foot
#
#     def ik(self, x, y, z):
#         """
#         Calculates the inverse kinematics from a given foot coordinate (x,y,z)[mm]
#         and returns the joint angles[degrees]
#
#         Reference (there are typos)
#         https://tote.readthedocs.io/en/latest/ik.html
#
#         If the foot (x,y,z) is in a position that does not produce a result (some
#         numeric error or invalid foot location), the this returns None.
#         """
#         # try:
#         Lc = self.coxaLength
#         Lf = self.femurLength
#         Lt = self.tibiaLength
#
#         if sqrt(x**2 + y**2) < Lc:
#             print('too short')
#             return None
#         # elif z > 0.0:
#         #     return None
#
#         a = atan2(y, x)
#         f = sqrt(x**2 + y**2) - Lc
#         # b1 = atan2(z, f)  # takes into account quadrent, z is neg
#
#         # you have different conditions depending if z is pos or neg
#         if z < 0.0:
#             b1 = atan2(f, fabs(z))
#         else:
#             b1 = atan2(z, f)
#
#         d = sqrt(f**2 + z**2)  # <---
#
#         # print('ik pos: {} {} {}'.format(x,y,z))
#         # print('d: {:.3f}  f: {:.3f}'.format(d,f))
#         # print('Lc Lf Lt: {} {} {}'.format(Lc,Lf,Lt))
#         # print('num: {:.3f}'.format(Lf**2 + d**2 - Lt**2))
#         # print('den: {:.3f}'.format(2.0 * Lf * d))
#         # print('acos: {:.2f}'.format((Lf**2 + d**2 - Lt**2) / (2.0 * Lf * d)))
#
#         guts = ((Lf**2 + d**2 - Lt**2) / (2.0 * Lf * d))
#         if 1.0 < guts or guts < -1.0:
#             print('acos crap!: {:.3f} {:.3f} {:.3f} guts: {:.3f}'.format(x, y, z, guts))
#             return None
#         b2 = acos((Lf**2 + d**2 - Lt**2) / (2.0 * Lf * d))  # issues?
#         b = b1 + b2
#         g = acos((Lf**2 + Lt**2 - d**2) / (2.0 * Lf * Lt))
#
#         # FIXES ###################################
#         g -= pi  # fix to align fk and ik frames
#
#         if z < 0.0:
#             b -= pi/2  #
#         ##############################################
#         # print('b1 b2: {:.2f} {:.2f}'.format(r2d(b1), r2d(b2)))
#         # print('ik angles: {:.2f} {:.2f} {:.2f}'.format(r2d(a), r2d(b), r2d(g)))
#         return r2d(a), r2d(b), r2d(g)  # coxaAngle, femurAngle, tibiaAngle
#
#         # except Exception as e:
#         #     print('ik error:', e)
#         #     raise e
#
#     def moveFoot(self, x, y, z):
#         """
#         Attempts to move it's foot to coordinates [x,y,z]
#         """
#         try:
#             # a, b, c = self.ik(x, y, z)  # inverse kinematics
#             # angles = [a, b, c]
#             angles = self.ik(x, y, z)  # inverse kinematics
#             # return angles
#             if angles is None:
#                 print('something bad')
#                 return
#             # print('angles: {:.2f} {:.2f} {:.2f}'.format(*angles))
#             for i, servo in enumerate(self.servos):
#                 # print('i, servo:', i, servo)
#                 angle = angles[i]
#                 # print('servo {} angle {}'.format(i, angle))
#                 servo.angle = angle
#             return angles
#
#         except Exception as e:
#             print (e)
#             raise
#
#     def moveFootAngles(self, a, b, c):
#         """
#         Attempts to move it's foot to coordinates [x,y,z]
#         """
#         try:
#             for servo, angle in zip(self.servos, (a, b, c)):
#                 servo.angle = angle
#
#         except Exception as e:
#             print('Leg::moveFootAngles() error:', e)
#             raise
#
#     # def reset(self):
#     #     # self.angles = self.resting_position
#     #     self.move(*self.foot0)
