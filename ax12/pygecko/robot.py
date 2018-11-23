#!/usr/bin/env python3
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
from pygecko.multiprocessing import geckopy
import sys
sys.path.insert(0,'../testing')
from Gait2 import Discrete
global_logger = None


def getHostSerialNumber():
    ssn = None
    a=check_output(["cat", '/proc/cpuinfo'])
    for s in a.split('\n'):
        if s.find('Serial') > -1:
            ssn = s.split()[2]
    return ssn


class RobotTest(object):
    def __init__(self, test=False):
        bcm_pin = None
        if test:  # manual override for testing - don't actually talk to servos
            ser = 'fake'
        elif platform.system() == 'Darwin':
            ser = '/dev/tty.usbserial-A506BOT5'
        elif platform.system() == 'Linux':
            ser = '/dev/serial0'
            bcm_pin = 11
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
        self.gait = Discrete(55.0, neutral)
        # self.gait.setLegLift(20)
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

    def handle_msg(self, topic, msg):
        # FIXME: make sure all topics are not binary
        try:
            topic = topic.decode('utf-8')
        except Exception:
            pass

        if topic == 'cmd':
            pts = self.gait.oneCycle(*msg)        # get 3d feet points
            # pts = self.gait.command(cmd)        # get 3d feet points

            # pts = (x,y,z) for each leg for the whole cycle
            # speed = max speed seen by any joint, most likely it will be lower
            angles_speeds = self.leg.generateServoAngles2(pts, 200)  # get servo angles

            # only move 1 leg, remove others from commands
            if False:
                angles_speeds.pop(2)
                angles_speeds.pop(1)
                angles_speeds.pop(3)

            self.engine.moveLegsGait4(angles_speeds)  # send commands to servos
        elif topic == 'avoid':
            # global_logger("avoid is not implemented yet")
            for meas in msg:
                # global_logger("lidar: {:.1f} deg    {:.1f} m", *meas)
                pass
        else:
            # global_logger("*** unsupported message ***")
            print("bad msg: {} {}".format(topic, msg))


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
        time.sleep(1)
        # feet = {}
        # for leg in range(4):
        #     print('d', self.engine.last_move[leg])  # these are servo angles!!!!
        #     x,y,z,s = self.engine.last_move[leg]
        #     feet[leg] = ((x,y,0),(80, 0, 1),)  # foot position in mm

        pt = ((130,0,0),(80, 0, 1),)  # foot position in mm
        feet = {
            0: pt,
            1: pt,
            2: pt,
            3: pt,
        }
        angles_speeds = self.leg.generateServoAngles2(feet, speed)
        self.engine.moveLegsGait3(angles_speeds)

    def stand(self, speed=100):
        """
        Puts legs into a standing position
        """
        # angles = self.positions['stand']
        # # ans = [x for x in self.positions['stand']]
        # ans = self.positions['stand']
        # feet = {
        #     0: [ans+[speed]],
        #     1: [ans+[speed]],
        #     2: [ans+[speed]],
        #     3: [ans+[speed]],
        # }
        #
        # print(feet)
        #
        # self.engine.moveLegsGait3(feet)
        # time.sleep(1)
        pt = ((130, 0, -70),)  # foot position in mm
        feet = {
            0: pt,
            1: pt,
            2: pt,
            3: pt,
        }
        angles_speeds = self.leg.generateServoAngles2(feet, speed)
        self.engine.moveLegsGait3(angles_speeds)
        time.sleep(1)


def go(**kwargs):
    geckopy.init_node(**kwargs)
    # global_logger = geckopy.log

    test = kwargs.get('test', True)
    robot = RobotTest(test)

    # s = geckopy.Subscriber(['cmd'], robot.handle_msg)
    geckopy.spin(5)


if __name__ == "__main__":
    kw = {}
    go(kwargs=kw)
