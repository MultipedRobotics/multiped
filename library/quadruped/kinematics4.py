##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
from math import sin, cos, acos, atan2, sqrt, pi
from math import radians as d2r
# from math import degrees as r2d
# import logging
# from quadruped.Servo import Servo

# logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.ERROR)

# from collections import namedtuple
#
# Link = namedtuple('Link', 'length offset')
# Leg4Info = namedtuple('Leg4Info', 'coxa femur tibia fibia tarsus')


# def ramp(val, length):
#     """
#     Simple triangle for scaling speed. it always returns 0.5 at the lowest
#     and is 1.0 at max in the middle
#
#     in: val - step
#         length - number of steps
#     out: 0.5 - 1.0
#     """
#     val = val % length
#     # print("ramp: {} {} {}".format(val, length/2, length))
#     slope = 0.5/(length/2)
#     if val > length/2:
#         # since it is symetric, just mirror the answer
#         val = (length - val)
#     return slope*val + 0.5


class KinematicsException(Exception):
    pass


class Kinematics4(object):
    """
    Leg class outputs the servo angles for some requested foot location (x,y,z)

    Leg knows:
    - leg dimensions
    - number of servos and their parameters/limits
    - fk/ik equations
    - sit/stand sequence
    """
    # these are fixed by the 3D printing, not changing
    coxaLength = None
    tibiaLength = None
    femurLength = None
    tarsusLength = None

    # positions = {
    #     'stand': None,
    #     # 'sit': None,
    #     # 'neutral': None
    # }

    def __init__(self, params):
        """
        Each leg has 4 servos/channels
        """
        # # setup kinematics and servos
        # self.servos = []
        # for ID, seg in enumerate(['coxa', 'femur', 'tibia', 'tarsus']):
        #     self.servos.append(Servo(ID, params[seg][1], params[seg][2]))

        self.coxaLength = params['coxa'][0]
        self.femurLength = params['femur'][0]
        self.tibiaLength = params['tibia'][0]
        self.tarsusLength = params['tarsus'][0]

        # if 'stand' in params:
        #     self.positions['neutral'] = self.forward(*params['stand'])
        # else:
        #     raise Exception('Need to have "stand" angles in params file')

    def __del__(self):
        pass

    def forward(self, t1, t2, t3, t4, degrees=True):
        """
        Forward kinematics of the leg, note, default angles are all degrees.
        The input angles are referenced to the DH frame arrangement.
        """
        l1 = self.coxaLength
        l2 = self.femurLength
        l3 = self.tibiaLength
        l4 = self.tarsusLength

        if degrees:
            t1 = d2r(t1)
            t2 = d2r(t2)
            t3 = d2r(t3)
            t4 = d2r(t4)

        x = (l1 + l2*cos(t2) + l3*cos(t2 + t3) + l4*cos(t2 + t3 + t4))*cos(t1)
        y = (l1 + l2*cos(t2) + l3*cos(t2 + t3) + l4*cos(t2 + t3 + t4))*sin(t1)
        z = l2*sin(t2) + l3*sin(t2 + t3) + l4*sin(t2 + t3 + t4)

        return (x, y, z,)

    def inverse(self, x, y, z, o=90, degrees=True):
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

        Most of the robot arm move in the plane defined by w-z

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
        def cosinelaw(a, b, c):
            # cosine law only used by this function
            # cos(g) = (a^2+b^2-c^2)/2ab
            try:
                ans = acos((a**2+b**2-c**2)/(2*a*b))
            except ValueError:
                print("num: {}".format(a**2+b**2-c**2))
                print("den: {}".format(2*a*b))
                print("acos({})".format((a**2+b**2-c**2)/(2*a*b)))
                raise
            return ans

        l1 = self.coxaLength
        l2 = self.femurLength
        l3 = self.tibiaLength
        l4 = self.tarsusLength

        t1 = atan2(y, x)

        if degrees:
            o = o*pi/180

        try:
            w = sqrt(x**2 + y**2) - l1
            j4w = w + l4*cos(o)
            j4z = z + l4*sin(o)
            r = sqrt(j4w**2 + j4z**2)
            g1 = atan2(j4z, j4w)
            g2 = cosinelaw(l2, r, l3)
            t2 = g1+g2

            t3 = pi+cosinelaw(l2, l3, r)

            j2w = l2*cos(t2)
            j2z = l2*sin(t2)
            c = sqrt((w-j2w)**2 + (z-j2z)**2)
            t4 = pi+cosinelaw(l3, l4, c)
        except Exception as e:
            print('inverse({:.2f},{:.2f},{:.2f},{:.2f})'.format(x, y, z, o))
            print('Error:', e)
            raise

        def check(t):
            if t > 150*pi/180:
                t -= 2*pi
            elif t < -150*pi/180:
                t += 2*pi
            return t

        # maxa = 150*pi/180
        # t1 = t1 if t1 <= maxa else t1-2*pi

        t1 = check(t1)  # value?? check elsewhere?
        t2 = check(t2)
        t3 = check(t3)
        t4 = check(t4)

        if degrees:
            t1 *= 180/pi
            t2 *= 180/pi
            t3 *= 180/pi
            t4 *= 180/pi

        return (t1, t2, t3, t4)

    def generateDHAngles(self, footLoc, speed):
        """
        This is a bulk process and takes all of the foot locations for an entire
        sequence of a gait cycle. It handles all legs at once.

        speed: this is the max movement speed

        footLoc: locations of feet from gait
        {      step0      step1   ...
            0: [(x,y,z), (x,y,z), ...] # leg0
            2: [(x,y,z), (x,y,z), ...] # leg2
            ...
        }

        return
        {      step 0          step 1         ...
            0: [(t1,t2,t3,t4,speed), (t1,t2,t3,t4,speed), ...] # leg0
            2: [(t1,t2,t3,t4,speed), (t1,t2,t3,t4,speed), ...] # leg2
            ...
        } where t=theta in DH space
        """

        # get the keys and figure out some stuff
        keys = list(footLoc.keys())
        angles = {}

        print("=[generateServoAngles2 speed servo[0-3]]===================")
        for legNum in keys:
            print("Leg[{}]-------------".format(legNum))
            pos = footLoc[legNum]  # grab foot positions for leg k
            angles[legNum] = []

            # calculate the inverse DH angles
            for step, p in enumerate(pos):
                s = self.inverse(*p)  # s0,s1,s2,s3
                scaled_speed = speed
                angles[legNum].append(s + (scaled_speed,))
                print("  {:2}: {} {:7.2f} {:7.2f} {:7.2f} {:7.2f}".format(step, scaled_speed, *s))

        return angles


    # def generateServoAngles(self, footLoc, speed):
    #     """
    #     This is a bulk process and takes all of the foot locations for an entire
    #     sequence of a gait cycle. It handles all legs at once.
    #
    #     speed: this is the max movement speed
    #
    #     footLoc: locations of feet from gait
    #     {      step0      step1   ...
    #         0: [(x,y,z), (x,y,z), ...] # leg0
    #         2: [(x,y,z), (x,y,z), ...] # leg2
    #         ...
    #     }
    #
    #     return
    #     {      step 0          step 1         ...
    #         0: [[(t1,s1),(t2,s2),(t3,s3),(t4,s4)], [(t1,s1),(t2,s2),(t3,s3),(t4,s4)], ...] # leg0
    #         2: [[(t1,s1),(t2,s2),(t3,s3),(t4,s4)], [(t1,s1),(t2,s2),(t3,s3),(t4,s4)], ...] # leg2
    #         ...
    #     } where t=theta s=speed
    #     """
    #     # FIXME: fix this to handle N legs, right now it only does 4
    #
    #     # get the keys and figure out some stuff
    #     keys = list(footLoc.keys())
    #     angles = {}
    #
    #     for k in keys:
    #         pos = footLoc[k]  # grab foot positions for leg k
    #         angles[k] = []
    #
    #         # calculate the inverse DH angles
    #         numStep = len(pos)
    #         for step, p in enumerate(pos):
    #             s = self.inverse(*p)  # s0,s1,s2,s3
    #             tmp = self.DH2Servo(s)
    #             # scaled_speed = int(speed*ramp(step, numStep))
    #             # if p[2] > -70: scaled_speed = speed
    #             # else: scaled_speed = int(0.6*speed)
    #             scaled_speed = speed
    #             tmp2 = [(x, scaled_speed) for x in tmp]
    #             angles[k].append(tmp2)
    #             # print("speed", speed)
    #             # print("tmp", tmp)
    #             # exit(0)
    #
    #     return angles


    # def generateServoAngles2(self, footLoc, speed):
    #     """
    #     This is a bulk process and takes all of the foot locations for an entire
    #     sequence of a gait cycle. It handles all legs at once.
    #
    #     speed: this is the max movement speed
    #
    #     footLoc: locations of feet from gait
    #     {      step0      step1   ...
    #         0: [(x,y,z), (x,y,z), ...] # leg0
    #         2: [(x,y,z), (x,y,z), ...] # leg2
    #         ...
    #     }
    #
    #     return
    #     {      step 0          step 1         ...
    #         0: [(t1,t2,t3,t4,speed), (t1,t2,t3,t4,speed), ...] # leg0
    #         2: [(t1,t2,t3,t4,speed), (t1,t2,t3,t4,speed), ...] # leg2
    #         ...
    #     } where t=theta
    #     """
    #
    #     # get the keys and figure out some stuff
    #     keys = list(footLoc.keys())
    #     angles = {}
    #
    #     print("=[generateServoAngles2 speed servo[0-3]]===================")
    #     for legNum in keys:
    #         print("Leg[{}]-------------".format(legNum))
    #         pos = footLoc[legNum]  # grab foot positions for leg k
    #         angles[legNum] = []
    #         # print('pos', pos)
    #
    #         # calculate the inverse DH angles
    #         # numStep = len(pos)
    #         for step, p in enumerate(pos):
    #             # print('  {:2}: {:7.2f} {:7.2f} {:7.2f}'.format(i, *pt))
    #             # print('step: {} p: {}'.format(step, p))
    #             s = self.inverse(*p)  # s0,s1,s2,s3
    #             tmp = self.DH2Servo(s)
    #             # scaled_speed = int(speed*ramp(step, numStep))
    #             # if p[2] > -70: scaled_speed = speed
    #             # else: scaled_speed = int(0.6*speed)
    #             # tmp2 = [(x, scaled_speed) for x in tmp]
    #             scaled_speed = speed
    #             angles[legNum].append(tmp + (scaled_speed,))
    #             # print("speed", speed)
    #             # print("tmp", tmp)
    #             # # exit(0)
    #             # print("  {:2}: {:7.2f} {:7.2f} {:7.2f} {:7.2f}".format(step, *tmp))
    #             print("  {:2}: {} {:7.2f} {:7.2f} {:7.2f} {:7.2f}".format(step, scaled_speed, *tmp))
    #
    #     return angles

    # def DH2Servo(self, angles):
    #     tmp = []
    #     for s, a in list(zip(self.servos, angles)):
    #         tmp.append(s.DH2Servo(a))
    #     return tuple(tmp)

    def pprint(self, step):
        print('*'*25)
        for leg in step:
            print('  DH: [{:.0f} {:.0f} {:.0f} {:.0f}]'.format(*leg))

    # def getNeutralPos(self):
    #     return self.positions['neutral']

    # def generateServoAngles_DH(self, angles):
    #     """
    #     This is a bulk process and takes all of the foot locations for an entire
    #     sequence of a gait cycle. It handles all legs at once.
    #
    #     footLoc: locations of feet from gait
    #     {      step0      step1   ...
    #         0: [[t1,t2,t3,t4], [t1,t2,t3,t4], ...] # leg0 DH space
    #         2: [[t1,t2,t3,t4], [t1,t2,t3,t4], ...] # leg2 DH space
    #         ...
    #     }
    #
    #     return
    #     {      step 0          step 1         ...
    #         0: [[t1,t2,t3,t4], [t1,t2,t3,t4], ...] # leg0 servo space
    #         2: [[t1,t2,t3,t4], [t1,t2,t3,t4], ...] # leg2 servo space
    #         ...
    #     }
    #     """
    #     # get the keys and figure out some stuff
    #     keys = list(footLoc.keys())
    #     angles = {}
    #
    #     for k in keys:
    #         angles[k] = []
    #         # calculate the inverse DH angles
    #         for s in angles:
    #             # tmp = [0]*4
    #             # tmp[0] = self.servos[0].DH2Servo(s[0])
    #             # tmp[1] = self.servos[1].DH2Servo(s[1])
    #             # tmp[2] = self.servos[2].DH2Servo(s[2])
    #             # tmp[3] = self.servos[3].DH2Servo(s[3])
    #             tmp = self.DH2Servo(s)
    #             angles[k].append(tmp)
    #
    #     return angles

    # def generateServoAngles(self, footLoc):
    #     """
    #     This is a bulk process and takes all of the foot locations for an entire
    #     sequence of a gait cycle. It handles all legs at once.
    #
    #     footLoc: locations of feet from gait
    #     {      step0      step1   ...
    #         0: [(x,y,z), (x,y,z), ...] # leg0
    #         2: [(x,y,z), (x,y,z), ...] # leg2
    #         ...
    #     }
    #
    #     return
    #     {      step 0          step 1         ...
    #         0: [[t1,t2,t3,t4], [t1,t2,t3,t4], ...] # leg0
    #         2: [[t1,t2,t3,t4], [t1,t2,t3,t4], ...] # leg2
    #         ...
    #     }
    #     """
    #     # get the keys and figure out some stuff
    #     keys = list(footLoc.keys())
    #     angles = {}
    #
    #     for k in keys:
    #         pos = footLoc[k]  # grab foot positions for leg k
    #         angles[k] = []
    #
    #         # calculate the inverse DH angles
    #         for p in pos:
    #             s = self.inverse(*p)  # s0,s1,s2,s3
    #             tmp = self.DH2Servo(s)
    #             angles[k].append(tmp)
    #
    #     return angles
