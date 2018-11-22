#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
from quadruped import Engine
# from quadruped import DiscreteRippleGait
from quadruped import Leg4
from pyservos import AX12
import time
from math import pi
import platform
from plotting import rplot, rplot2,plot_body_frame
from Gait2 import Discrete

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
        self.gait = Discrete(55.0, neutral)
        self.gait.scale = 65
        # self.engine = Engine(data, AX12, wait=0.3, bcm_pin=bcm_pin)

    def go(self):
        # cmd = [x, y, rotation_z]
        # pts = array(3d foot locations)
        cmd = [1,0,0]
        pts = self.gait.oneCycle(*cmd)
        # plot_body_frame(pts,1)

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

        rplot2(a)

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
