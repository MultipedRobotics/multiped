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


class RobotTest(object):
    def __init__(self):
        bcm_pin = None
        if True:  # manual override for testing - don't actually talk to servos
            ser = 'fake'
        elif platform.system() == 'Darwin':
            ser = '/dev/tty.usbserial-A506BOT5'
        elif platform.system() == 'Linux':
            ser = '/dev/serial0'
            bcm_pin = 4
        else:
            raise Exception('Your OS is not supported')

        data = {
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
        self.leg = Leg4(data)
        neutral = self.leg.getNeutralPos()
        self.gait = DiscreteRippleGait(55.0, neutral)
        self.gait.setLegLift(60)
        self.gait.scale = 65
        self.engine = Engine(data, AX12, wait=0.3, bcm_pin=bcm_pin)

        self.positions = {
            'stand': None,
            'sit': None
        }

        for key in ['stand', 'sit']:
            if key in data:
                angles = []
                for a, s in zip(data[key], self.leg.servos):
                    angles.append(s.DH2Servo(a))
                self.positions[key] = angles

        self.stand()

    def __del__(self):
        self.sit()

    def pose_pt(self, leg, pt, speed):
        """
        Moves 1 leg to a position
        value?
        """
        pts = {
            leg: [pt]
        }
        angles = self.leg.generateServoAngles(pts, speed)
        print(angles)
        self.engine.moveLegsGait(angles)

    def walk(self):
        print(" <<< Walk >>>")
        # predefined walking path
        # x, y, rotation
        path = [
            [1.0, 0, 0],
            # [1.0, 0, 0],
            # [1.0, 0, 0],
            # [1.0, 0, 0],
            # [1.0, 0, 0],
            # [1.0, 0, 0],
            # [1.0, 0, 0],
            # [1.0, 0, 0],
            # [1.0, 0, 0],
            # [1.0, 0, 0],
            # [0, 0, pi/4],
            # [0, 0, pi/4],
            # [0, 0, pi/4],
            # [0, 0, -pi/4],
            # [0, 0, -pi/4],
            # [0, 0, -pi/4],
            # [-1.0, 0, 0],
            # [-1.0, 0, 0],
            # [-1.0, 0, 0],
            # [-1.0, 0, 0],
            # [-1.0, 0, 0],
            # [-1.0, 0, 0],
            # [-1.0, 0, 0],
            # [-1.0, 0, 0],
            # [-1.0, 0, 0],
            # [-1.0, 0, 0],
        ]

        for cmd in path:
            pts = self.gait.oneCycle(*cmd)        # get 3d feet points
            # pts = self.gait.command(cmd)        # get 3d feet points
            angles_speeds = self.leg.generateServoAngles(pts, 100)  # get servo angles
            # print("angles_speeds", angles_speeds)

            # only move 1 leg, remove others from commands
            # angles.pop(0)
            # angles.pop(1)
            # angles.pop(3)

            self.engine.moveLegsGait(angles_speeds)  # send commands to servos
            # time.sleep(5)
            # print(cmd)
            # print(angles)
            # print('len', len(angles[2]))

    def step(self, leg, p1, p2, lift):
        """
        Pick the foot up and set it down
        leg - which leg number 0-3
        p1 - start (x,y,z)
        p2 - stop (x,y,z)
        lift - how high to lift the foot
        """
        pass

    def sit(self, speed=100):
        """
        Puts legs into a sitting position
        """
        # angles = self.leg.sit()
        ans = [(x, speed) for x in self.positions['sit']]
        feet = {
            0: [ans],
            1: [ans],
            2: [ans],
            3: [ans],
        }

        self.engine.moveLegsGait(feet)
        time.sleep(1)

    def stand(self, speed=100):
        """
        Puts legs into a standing position
        """
        # angles = self.positions['stand']
        ans = [(x, speed) for x in self.positions['stand']]
        feet = {
            0: [ans],
            1: [ans],
            2: [ans],
            3: [ans],
        }

        self.engine.moveLegsGait(feet)
        time.sleep(1)


def main():
    test = RobotTest()
    # time.sleep(2)

    try:
        # test.stand()
        # time.sleep(3)
        test.walk()
        # test.sitstand()
        # test.pose_pt(2,[140,0,-10])
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
