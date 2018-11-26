#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
from quadruped import Engine
from quadruped import DiscreteRippleGait
from quadruped import Leg4
from pyservos import AX12
import time
from math import pi
import platform
from plotting import rplot, rplot2,plot_body_frame

"""
Azimuth angle is between x and w and lies in the x-y plane

           ^ x
     w     |
       \   |
     l1 \  |
         \ |
          \|
<----------+ (z is out of the page - right hand rule)
y

Most of the leg moves in the plane defined by w-z

^ z      l3
|      o-----o
|     /       \ l4
|    / l2      E
|   /
+--o-------------> w
 l1

l1: coxa
l2: femur
l3: tibia
l4: tarsus

All joint angles returned are in degrees: (t1, t2, t3, t4)
"""

# class RobotTest(object):
#     def __init__(self):
#         bcm_pin = None
#         ser = 'fake'
#
#         data = {
#             # [ length, (limit_angles), offset_angle] - units:mm or degrees
#             'coxa':   [52, [-90, 90], 150],
#             'femur':  [90, [-90, 90], 123],   # fixme
#             'tibia':  [89, [-90, 120], 194],  # fixme
#             'tarsus': [90, [-90, 90], 167],
#
#             # gait
#             # Angles: 0.00 75.60 -120.39 -45.22
#             # 'stand': [0, 75, -120, -45],
#             # 'stand': [0, 37, -139, -45],
#             # 'standUnits': 'deg',
#             'stand': [0, 160-123, 130-194, 100-167],
#             'sit': [0, 250-123, 80-194, 60-167],
#
#             # engine
#             'serialPort': ser,
#             # 'write': 'bulk'
#         }
#         self.leg = Leg4(data)
#         neutral = self.leg.getNeutralPos()
#         self.gait = DiscreteRippleGait(55.0, neutral)
#         self.gait.setLegLift(20)
#         self.gait.scale = 65
#         self.engine = Engine(data, AX12, wait=0.3, bcm_pin=bcm_pin)
#
#         self.positions = {
#             'stand': None,
#             'sit': None
#         }

        # for key in ['stand', 'sit']:
        #     if key in data:
        #         angles = []
        #         for a, s in zip(data[key], self.leg.servos):
        #             angles.append(s.DH2Servo(a))
        #         self.positions[key] = angles
        #
        # self.stand()

    # def __del__(self):
    #     self.sit()
    #
    # def pose_pt(self, leg, pt, speed):
    #     """
    #     Moves 1 leg to a position
    #     value?
    #     """
    #     pts = {
    #         leg: [pt]
    #     }
    #     angles = self.leg.generateServoAngles2(pts, speed)
    #     print(angles)
    #     self.engine.moveLegsGait3(angles)
    #     time.sleep(1)
    #
    # def angleCheckLeg(self, legNum, speed):
    #     """
    #     speed = 1 - 1023 (scalar, all servos move at same rate)
    #     {      step 0          step 1         ...
    #         0: [(t1,t2,t3,t4,speed), (t1,t2,t3,t4,speed), ...] # leg0
    #         2: [(t1,t2,t3,t4,speed), (t1,t2,t3,t4,speed), ...] # leg2
    #         ...
    #     } where t=theta
    #     """
    #     cmds = {}
    #     dh_cmds = [
    #         [0, 0, 0, 0],
    #         [0, 0, 0, 45],
    #         [0, 0, 0, -45],
    #         [0, 0, 0, 0],
    #         [0, 0, 90, 0],
    #         [0, 0, 0, 0],
    #         [0, 90, 0, 0],
    #         [0, 0, 0, 0],
    #         [80, 0, 0, 0],
    #         [-80, 0, 0, 0],
    #         [0, 0, 0, 0],
    #     ]
    #
    #     move = []
    #     for angles in dh_cmds:
    #         s_cmds = []
    #         for a, s in zip(angles, self.leg.servos):
    #             s_cmds.append(s.DH2Servo(a))
    #         s_cmds.append(speed)
    #         move.append(s_cmds)
    #     cmds[legNum] = move
    #     print(cmds)
    #     self.engine.moveLegsGait3(cmds)

    # def walk(self):
    #     print(" <<< Walk >>>")
    #     # predefined walking path
    #     # x, y, rotation
    #     path = [
    #         [1.0, 0, 0],
    #         # [1.0, 0, 0],
    #         # [1.0, 0, 0],
    #         # [1.0, 0, 0],
    #         # [1.0, 0, 0],
    #         # [1.0, 0, 0],
    #         # [1.0, 0, 0],
    #         # [1.0, 0, 0],
    #         # [1.0, 0, 0],
    #         # [1.0, 0, 0],
    #         # [0, 0, pi/4],
    #         # [0, 0, pi/4],
    #         # [0, 0, pi/4],
    #         # [0, 0, -pi/4],
    #         # [0, 0, -pi/4],
    #         # [0, 0, -pi/4],
    #         # [-1.0, 0, 0],
    #         # [-1.0, 0, 0],
    #         # [-1.0, 0, 0],
    #         # [-1.0, 0, 0],
    #         # [-1.0, 0, 0],
    #         # [-1.0, 0, 0],
    #         # [-1.0, 0, 0],
    #         # [-1.0, 0, 0],
    #         # [-1.0, 0, 0],
    #         # [-1.0, 0, 0],
    #     ]
    #
    #     for cmd in path:
    #         pts = self.gait.oneCycle(*cmd)        # get 3d feet points
    #         # pts = self.gait.command(cmd)        # get 3d feet points
    #
    #         # pts = (x,y,z) for each leg for the whole cycle
    #         # speed = max speed seen by any joint, most likely it will be lower
    #         angles_speeds = self.leg.generateServoAngles2(pts, 200)  # get servo angles
    #
    #         # # only move 1 leg, remove others from commands
    #         # if False:
    #         #     angles_speeds.pop(2)
    #         #     angles_speeds.pop(1)
    #         #     angles_speeds.pop(3)
    #
    #         self.engine.moveLegsGait4(angles_speeds)  # send commands to servos

    # def step(self, leg, p1, p2, lift):
    #     """
    #     Pick the foot up and set it down
    #     leg - which leg number 0-3
    #     p1 - start (x,y,z)
    #     p2 - stop (x,y,z)
    #     lift - how high to lift the foot
    #     """
    #     pass
    #
    # def sit(self, speed=100):
    #     """
    #     Puts legs into a sitting position
    #     """
    #     time.sleep(1)
    #     # feet = {}
    #     # for leg in range(4):
    #     #     print('d', self.engine.last_move[leg])  # these are servo angles!!!!
    #     #     x,y,z,s = self.engine.last_move[leg]
    #     #     feet[leg] = ((x,y,0),(80, 0, 1),)  # foot position in mm
    #
    #     pt = ((130,0,0),(80, 0, 1),)  # foot position in mm
    #     feet = {
    #         0: pt,
    #         1: pt,
    #         2: pt,
    #         3: pt,
    #     }
    #     angles_speeds = self.leg.generateServoAngles2(feet, speed)
    #     self.engine.moveLegsGait3(angles_speeds)
    #
    # def stand(self, speed=100):
    #     """
    #     Puts legs into a standing position
    #     """
    #     # angles = self.positions['stand']
    #     # # ans = [x for x in self.positions['stand']]
    #     # ans = self.positions['stand']
    #     # feet = {
    #     #     0: [ans+[speed]],
    #     #     1: [ans+[speed]],
    #     #     2: [ans+[speed]],
    #     #     3: [ans+[speed]],
    #     # }
    #     #
    #     # print(feet)
    #     #
    #     # self.engine.moveLegsGait3(feet)
    #     # time.sleep(1)
    #     pt = ((130, 0, -70),)  # foot position in mm
    #     feet = {
    #         0: pt,
    #         1: pt,
    #         2: pt,
    #         3: pt,
    #     }
    #     angles_speeds = self.leg.generateServoAngles2(feet, speed)
    #     self.engine.moveLegsGait3(angles_speeds)
    #     time.sleep(1)



class RobotTest(object):
    def __init__(self):
        bcm_pin = None
        ser = 'fake'

        data = {
            # offsets for legs:
            # coxa: 150 deg
            # femur: 27 deg
            # tibia: 71-27=44
            # tarsus: 17
            # [ length, (limit_angles), offset_angle] - units:mm or degrees
            'coxa':   [52, [-90, 90], 150],
            'femur':  [90, [-90, 90], 123],   # fixme
            'tibia':  [89, [-90, 120], 194],  # fixme
            'tarsus': [90, [-90, 90], 167],

            # gait
            # Angles: 0.00 75.60 -120.39 -45.22
            # 'stand': [0, 75, -120, -45],
            # 'stand': [0, 37, -139, -45],
            # 'standUnits': 'deg',
            'stand': [0, 160-123, 130-194, 100-167],
            'sit': [0, 250-123, 80-194, 60-167],

            # engine
            'serialPort': ser,
            # 'write': 'bulk'
        }

        self.data = data

        self.leg = Leg4(data)
        neutral = self.leg.getNeutralPos()
        self.gait = DiscreteRippleGait(55.0, neutral)
        self.gait.setLegLift(20)
        self.gait.scale = 65
        # self.engine = Engine(data, AX12, wait=0.3, bcm_pin=bcm_pin)

    def go(self):
        # cmd = [x, y, rotation_z]
        # pts = array(3d foot locations)
        cmd = [1,0,0]
        pts = self.gait.oneCycle(*cmd)
        plot_body_frame(pts)
        # for k,v in pts.items():
        #     print('Leg', k)
        #     for p in v:
        #         print('  {}'.format(p))
        #
        # print('>> pts[0]', pts[0][0])

        # servo angles corrects for link offsets
        # angles_speeds is a dict = {
        #     0: [(t0,t1,t2,t3,speed), ...]
        #     1: ...
        # }

        m = self.data["coxa"][2]
        n = self.data["femur"][2]
        o = self.data["tibia"][2]
        p = self.data["tarsus"][2]

        angles_speeds = self.leg.generateServoAngles2(pts, 200)
        a = [(x[0]-m, x[1]-n, x[2]-o, x[3]-p,) for x in angles_speeds[0]]

        # for i in range(len(a)):
        #     # correct for offsets
        #     t1 = a[i][0] - self.data["coxa"][2]
        #     t2 = a[i][1] - self.data["femur"][2]
        #     t3 = a[i][2] - self.data["tibia"][2]
        #     t4 = a[i][3] - self.data["tarsus"][2]
        #     rplot(t1,t2,t3,t4)

        # rplot2(a)

    def test(self):
        """
        neutral: (196.89869392004982, 0.0, -76.0225669165195)
        >> rplot angles
         0: 0.000000 1: 40.867062 2: -71.172404 3: -59.694658
        """
        neutral = self.leg.getNeutralPos()
        print('neutral:', neutral)
        a = self.leg.inverse(*neutral)
        rplot(*a)


def main():
    test = RobotTest()

    try:
        # test.stand()
        # time.sleep(3)
        test.go()
        # test.angleCheckLeg(0, 200)
        # test.sitstand()
        # test.pose_pt(0, [160, 0, 30], 100)
        # a = [0, 160-123, 130-194, 100-167]
        # print(test.get_point(a))  # (196.89869392004982, 0.0, -76.0225669165195)
        # p = [160,0,-70]
        # print(test.get_angle(p))
        # test.sit()
        # time.sleep(2)
    except KeyboardInterrupt:
        print('bye ...')
        # time.sleep(1)


if __name__ == '__main__':
    main()
