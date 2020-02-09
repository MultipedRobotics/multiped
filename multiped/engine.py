##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
from pyservos import ServoSerial
from pyservos import Packet
# from pyservos import ServoTypes
from pyservos.packet import angle2int
from pyservos.utils import le
from multiped.Servo import Servo
import time

debug = True


def dprint(s):
    global debug
    if debug:
        print(s)


def calc_rpm(da, wait):
    """
    Given an angular delta and a wait time, calculate the rpm needed to achieve

    [Join Mode]
    0 ~ 1,023(0x3FF) can be used, and the unit is about 0.111rpm.
    If it is set to 0, it means the maximum rpm of the motor is used
    without controlling the speed. If it is 1023, it is about 114rpm.
    For example, if it is set to 300, it is about 33.3 rpm.

    AX12 max rmp is 59 (max speed 532)
    rev  min     360 deg      deg
    --- -------  ------- = 6 ----
    min  60 sec    rev        sec

    rpm = abs(new_angle - old_angle)/(0.111 * wait * 6)
    """
    return int(abs(da)/(0.111*wait*6))


def calc_wait(da, speed):
    """
    Given an angular delta and the speed (servo counts), calculate the how long
    to wait for the servo to complete the movement

    [Join Mode]
    0 ~ 1,023(0x3FF) can be used, and the unit is about 0.111rpm.
    If it is set to 0, it means the maximum rpm of the motor is used
    without controlling the speed. If it is 1023, it is about 114rpm.
    For example, if it is set to 300, it is about 33.3 rpm.

    AX12 max rmp is 59 (max speed 532)
    rev  min     360 deg      deg
    --- -------  ------- = 6 ----
    min  60 sec    rev        sec

                            da deg
    wait = ----------------------------------------
                 rpm                360 deg    min
           0.111 --- * speed_cnt *  ------- * ------
                 cnt                   rev    60 sec

    wait = abs(new_angle - old_angle)/(0.111 * speed * 6)
    """
    try:
        w = abs(da)/(0.111*speed*6)
    except ZeroDivisionError:
        w = 1
        print("*** calc_wait() div error: {}".format(speed))

    return w


class Engine(object):
    """
    This class holds the serial port and talks to the hardware. Other classes (
    e.g., gait, legs and servos) do the calculations for walking.
    """

    last_move = None

    def __init__(self, data, servoType):
        """
        data: serial port to use, if none, then use dummy port
        servoType: AX12 or XL320 or other servo type
        curr_pos: current leg position
        bcm_pin: which gpio pin is used for the comm
            {
                0: [(t0,t1,t2,t3,speed), ...]
                1: [...]
                ...
                3: [...]
            }
        """
        if 'bcm_pin' in data:
            bcm_pin = data['bcm_pin']
        else:
            bcm_pin = None

        # self.wait = wait
        # determine serial port
        # default to fake serial port
        if 'serialPort' in data:
            try:
                self.serial = ServoSerial(data['serialPort'], pi_pin=bcm_pin)
                print('Using servo serial port: {}'.format(data['serialPort']))
                self.serial.open()

            except Exception as e:
                print(e)
                print('Engine::init(): bye ...')
                exit(1)
        else:
            print('*** Using dummy serial port!!! ***')
            self.serial = ServoSerial('dummy')
            # raise Exception('No serial port given')

        # handle servos ... how does it know how many servos???
        self.servos_up = {}  # check servos are operating
        self.servos = []
        for ID, seg in enumerate(['coxa', 'femur', 'tibia', 'tarsus']):
            length, offset = data[seg]
            self.servos.append(Servo(ID, offset))
            # resp = self.pingServo(ID)  # return: (T/F, servo_angle)
            # self.servos[ID] = resp[0]
            # curr_angle[ID] =
        # for s, val in self.servos.items():
        #     if val is False:
        #         print("*** Engine.__init__(): servo[{}] has failed".format(s))

        self.packet = Packet(servoType)

        # keep track of last location, this is servo angle space
        # self.last_move = {
        #     0: curr_pos[0][0],
        #     1: curr_pos[1][0],
        #     2: curr_pos[2][0],
        #     3: curr_pos[3][0]
        # }
        self.last_move = self.getCurrentAngles()

    def getCurrentAngles(self):
        """
        Returns the current angles for all servos in DH space as a dictionary.
        angles = {
            0: [0.0, 130.26, -115.73, -104.52],
            1: [0.0, 130.26, -115.73, -104.52],
            2: [0.0, 130.26, -115.73, -104.52],
            3: [0.0, 130.26, -115.73, -104.52],
        }

        FIXME: actually query the servos and get there angles in DH space
        """
        angles = {
            0: [0.0, 130.26, -115.73, -104.52],
            1: [0.0, 130.26, -115.73, -104.52],
            2: [0.0, 130.26, -115.73, -104.52],
            3: [0.0, 130.26, -115.73, -104.52],
        }
        return angles

    def DH2Servo(self, angle, num):
        return self.servos[num].DH2Servo(angle)

    def moveLegsGait4(self, legs):
        """
        gait or sequence?
        speed = 1 - 1023 (scalar, all servos move at same rate)
        {      step 0          step 1         ...
            0: [(t1,t2,t3,t4,speed), (t1,t2,t3,t4,speed), ...] # leg0
            2: [(t1,t2,t3,t4,speed), (t1,t2,t3,t4,speed), ...] # leg2
            ...
        } where t=theta
        NOTE: each leg needs the same number of steps and servos per leg
        WARNING: these angles are in servo space [0-300 deg]

        [Join Mode]
        0 ~ 1,023(0x3FF) can be used, and the unit is about 0.111rpm.
        If it is set to 0, it means the maximum rpm of the motor is used
        without controlling the speed. If it is 1023, it is about 114rpm.
        For example, if it is set to 300, it is about 33.3 rpm.

        AX12 max rmp is 59 (max speed 532)
        rev  min     360 deg      deg
        --- -------  ------- = 6 ----
        min  60 sec    rev        sec

        sleep time = | (new_angle - old_angle) /(0.111 * min_speed * 6) |
        """
        # get the keys and figure out some stuff
        keys = list(legs.keys())  # which legs are we moving
        numSteps = len(legs[keys[0]])  # how many steps in the cycle
        numServos = len(legs[keys[0]][0])-1  # how many servos per leg, -1 because speed there

        # if self.last_move is None:
        #     # assume we just turned on and was in the sit position
        #     # need a better solution
        #     self.last_move = {
        #         0: legs[0][0],
        #         1: legs[1][0],
        #         2: legs[2][0],
        #         3: legs[3][0]
        #     }

        # curr_move = {}
        # for each step in legs
        for step in range(numSteps):
            # dprint("\nStep[{}]===============================================".format(step))
            data = []

            # find max time we have to wait for all 4 legs to reach their end
            # point.
            max_wait = 0
            for legNum in keys:
                angles = legs[legNum][step][:4]
                speed = legs[legNum][step][4]
                # print(" speed", speed)
                for a, oa in zip(angles, self.last_move[legNum][:4]):
                    da = abs(a-oa)
                    w = calc_wait(da, speed)
                    # print(" calc_wait: {:.3f}".format(w))
                    # print("calc_wait: {}".format(w))
                    max_wait = w if w > max_wait else max_wait

            # print(">> found wait", max_wait, " speed:", speed)

            servo_speeds = [100,125,150,200]

            # for legNum in [0,3,1,2]:
            for legNum in keys:
                # dprint("  leg[{}]--------------".format(legNum))
                leg_angles_speed = legs[legNum][step]
                # print(leg_angles_speed)
                angles = leg_angles_speed[:4]  # 4 servo angles
                speed = leg_angles_speed[4]
                # print("Speed:", speed, "wait", max_wait)

                for i, DH_angle in enumerate(angles):
                    # oldangle = self.last_move[legNum][i]
                    # due to rounding errors, to ensure the other servers finish
                    # BEFORE time.sleep(max_wait) ends, the the function it
                    # has less time
                    # spd = calc_rpm((angle - oldangle), 0.9*max_wait)
                    # now that i am scaling the spd parameter above, I sometimes
                    # exceed the original speed number, so saturate it if
                    # necessary
                    # spd = spd if spd <= speed else speed
                    # sl, sh = le(spd)
                    sl, sh = le(servo_speeds[i])
                    servo_angle = self.DH2Servo(DH_angle, i)
                    al, ah = angle2int(servo_angle)  # angle
                    data.append([legNum*numServos + i+1, al, ah, sl, sh])  # ID, low angle, high angle, low speed, high speed
                    # data.append([legNum*numServos + i+1, al, ah])  # ID, low angle, high angle, low speed, high speed

                self.last_move[legNum] = leg_angles_speed

            pkt = self.packet.makeSyncWritePacket(self.packet.base.GOAL_POSITION, data)
            self.serial.write(pkt)
            dprint("sent serial packet leg: {}".format(legNum))
            data = []
            print('max_wait', max_wait)
            time.sleep(max_wait)

            # time.sleep(1)



    # def pprint(self, i, step):
    #     print('***', i, '*'*25)
    #     for leg in step:
    #         print('  Servo: [{:.0f} {:.0f} {:.0f} {:.0f}]'.format(*leg))

    # def setServoSpeed(self, speed):
    #     """
    #     Sets the servo speed for all servos.
    #     speed - 0-1023, but only up to max speed of servo
    #     """
    #     # make packet function
    #     pkt = self.packet.makeWritePacket(
    #         self.packet.base.BROADCAST_ADDR,
    #         self.packet.base.GOAL_VELOCITY,
    #         le(speed)
    #     )
    #     self.serial.write(pkt)

    # def moveLegsGait(self, legs):
    #     """
    #     gait or sequence?
    #     speed = 1 - 1023 (scalar, all servos move at same rate)
    #     {      step 0          step 1         ...
    #         0: [[(t1,s1),(t2,s2),(t3,s3),(t4,s4)], [(t1,s1),(t2,s2),(t3,s3),(t4,s4)], ...] # leg0
    #         2: [[(t1,s1),(t2,s2),(t3,s3),(t4,s4)], [(t1,s1),(t2,s2),(t3,s3),(t4,s4)], ...] # leg2
    #         ...
    #     } where t=theta s=speed
    #     NOTE: each leg needs the same number of steps and servos per leg
    #     WARNING: these angles are in servo space [0-300 deg]
    #     """
    #     # get the keys and figure out some stuff
    #     keys = list(legs.keys())
    #     numSteps = len(legs[keys[0]])
    #     numServos = len(legs[keys[0]][0])
    #     # wait = self.wait  # FIXME: wait should be a function of speed
    #
    #     if self.last_move is None:
    #         # assume we just turned on and was in the sit position
    #         self.last_move = {}
    #     #     self.last_move = {
    #     #         # 0: [[(t1,s1),(t2,s2),(t3,s3),(t4,s4)]
    #     #         0: None,  # tuple of angles for each leg
    #     #         1: None,
    #     #         2: None,
    #     #         3: None
    #     #     }
    #     curr_move = {}
    #     # else:
    #     #     ts = 0
    #     #     for nleg, oleg in zip(legs, self.last_move):
    #     #         for
    #
    #     # for each step in legs
    #     # print("-------------------")
    #     for s in range(numSteps):
    #         dprint("\nStep[{}]===============================================".format(s))
    #         min_speed = 10000
    #         max_angle = 0
    #         data = []
    #         for legNum in keys:
    #             dprint("  leg[{}]--------------".format(legNum))
    #             step = legs[legNum][s]
    #             # print("step", step)
    #             curr_move[legNum] = step  # save current angle/speed
    #             for i, (angle, speed) in enumerate(step):
    #                 al, ah = angle2int(angle)  # angle
    #
    #                 # remember, servo IDs start at 1 not 0, so there is a +1
    #                 min_speed = speed if speed < min_speed else min_speed
    #                 max_angle = angle if angle > max_angle else max_angle
    #                 sl, sh = le(speed)
    #                 dprint("    Servo[{}], angle: {:.2f}, speed: {} time: {:.2f}".format(legNum*numServos + i+1, angle, speed, 0.111*speed*6))
    #                 data.append([legNum*numServos + i+1, al, ah, sl, sh])  # ID, low angle, high angle, low speed, high speed
    #
    #             pkt = self.packet.makeSyncWritePacket(self.packet.base.GOAL_POSITION, data)
    #             self.serial.write(pkt)
    #             dprint("sent serial packet")
    #             data = []
    #
    #         """
    #         [Join Mode]
    #         0 ~ 1,023(0x3FF) can be used, and the unit is about 0.111rpm.
    #         If it is set to 0, it means the maximum rpm of the motor is used
    #         without controlling the speed. If it is 1023, it is about 114rpm.
    #         For example, if it is set to 300, it is about 33.3 rpm.
    #
    #         AX12 max rpm is 59 (max speed 532)
    #         rev  min     360 deg      deg
    #         --- -------  ------- = 6 ----
    #         min  60 sec    rev        sec
    #
    #         sleep time = | (new_angle - old_angle) /(0.111 * min_speed * 6) |
    #         """
    #
    #         max_wait = 0
    #         if self.last_move:
    #             for legNum in curr_move.keys():
    #                 for (na, ns), (oa, os) in list(zip(curr_move[legNum], self.last_move[legNum])):
    #                     w = abs((na - oa)/(0.111*ns*6))
    #                     w *= 1.10  # scaling to make things look better: 1.3
    #                     max_wait = w if w > max_wait else max_wait
    #                 self.last_move[legNum] = curr_move[legNum]
    #         else:
    #             # this should only get called after start, when last_move = None
    #             self.last_move = curr_move
    #             max_wait = 1.0
    #
    #         # wait = 20 / (0.111*min_speed*6)
    #         time.sleep(max_wait)
    #         # print('[{}] max_wait: {:.3f}'.format(s, max_wait))
    #         print('max_wait', max_wait)
    #         # print('max_angle', max_angle)
    #
    # def moveLegsGait2(self, legs):
    #     """
    #     gait or sequence?
    #     speed = 1 - 1023 (scalar, all servos move at same rate)
    #     {      step 0          step 1         ...
    #         0: [(t1,t2,t3,t4,speed), (t1,t2,t3,t4,speed), ...] # leg0
    #         2: [(t1,t2,t3,t4,speed), (t1,t2,t3,t4,speed), ...] # leg2
    #         ...
    #     } where t=theta
    #     NOTE: each leg needs the same number of steps and servos per leg
    #     WARNING: these angles are in servo space [0-300 deg]
    #
    #     [Join Mode]
    #     0 ~ 1,023(0x3FF) can be used, and the unit is about 0.111rpm.
    #     If it is set to 0, it means the maximum rpm of the motor is used
    #     without controlling the speed. If it is 1023, it is about 114rpm.
    #     For example, if it is set to 300, it is about 33.3 rpm.
    #
    #     AX12 max rmp is 59 (max speed 532)
    #     rev  min     360 deg      deg
    #     --- -------  ------- = 6 ----
    #     min  60 sec    rev        sec
    #
    #     sleep time = | (new_angle - old_angle) /(0.111 * min_speed * 6) |
    #     """
    #     # get the keys and figure out some stuff
    #     keys = list(legs.keys())  # which legs are we moving
    #     numSteps = len(legs[keys[0]])  # how many steps in the cycle
    #     numServos = len(legs[keys[0]][0])-1  # how many servos per leg, -1 because speed there
    #
    #     if self.last_move is None:
    #         # assume we just turned on and was in the sit position
    #         # need a better solution
    #         self.last_move = {
    #             0: legs[0][0],
    #             1: legs[1][0],
    #             2: legs[2][0],
    #             3: legs[3][0]
    #         }
    #
    #     # curr_move = {}
    #     # for each step in legs
    #     for step in range(numSteps):
    #         dprint("\nStep[{}]===============================================".format(step))
    #         data = []
    #
    #         # for legNum in [0,3,1,2]:
    #         for legNum in keys:
    #             dprint("  leg[{}]--------------".format(legNum))
    #             leg_angles_speed = legs[legNum][step]
    #             # print(leg_angles_speed)
    #             angles = leg_angles_speed[:4]
    #             speed = leg_angles_speed[4]
    #             sl, sh = le(speed)
    #
    #             max_wait = 0
    #             for i, angle in enumerate(angles):
    #                 al, ah = angle2int(angle)  # angle
    #                 dprint("    Servo[{}], angle: {:.2f}, speed: {}".format(legNum*numServos + i+1, angle, speed))
    #                 data.append([legNum*numServos + i+1, al, ah, sl, sh])  # ID, low angle, high angle, low speed, high speed
    #
    #                 # print(self.last_move)
    #                 # print(leg_angles_speed)
    #                 # print(angles)
    #                 # print(i)
    #                 # print(legNum*numServos + i+1)
    #
    #                 oldangle = self.last_move[legNum][i]
    #                 # calculate wait time for a leg, take max time
    #                 w = abs((angle - oldangle)/(0.111*speed*6))
    #                 # print(angle - oldangle)
    #                 # print('w',w)
    #                 w *= 1.10  # scaling to make things look better: 1.3
    #                 max_wait = w if w > max_wait else max_wait
    #
    #             pkt = self.packet.makeSyncWritePacket(self.packet.base.GOAL_POSITION, data)
    #             self.serial.write(pkt)
    #             dprint("sent serial packet leg: {}".format(legNum))
    #             data = []
    #             print('max_wait', max_wait)
    #             time.sleep(max_wait)
    #
    #             self.last_move[legNum] = leg_angles_speed
    #
    # def moveLegsGait3(self, legs):
    #     """
    #     gait or sequence?
    #     speed = 1 - 1023 (scalar, all servos move at same rate)
    #     {      step 0          step 1         ...
    #         0: [(t1,t2,t3,t4,speed), (t1,t2,t3,t4,speed), ...] # leg0
    #         2: [(t1,t2,t3,t4,speed), (t1,t2,t3,t4,speed), ...] # leg2
    #         ...
    #     } where t=theta
    #     NOTE: each leg needs the same number of steps and servos per leg
    #     WARNING: these angles are in servo space [0-300 deg]
    #
    #     [Join Mode]
    #     0 ~ 1,023(0x3FF) can be used, and the unit is about 0.111rpm.
    #     If it is set to 0, it means the maximum rpm of the motor is used
    #     without controlling the speed. If it is 1023, it is about 114rpm.
    #     For example, if it is set to 300, it is about 33.3 rpm.
    #
    #     AX12 max rmp is 59 (max speed 532)
    #     rev  min     360 deg      deg
    #     --- -------  ------- = 6 ----
    #     min  60 sec    rev        sec
    #
    #     sleep time = | (new_angle - old_angle) /(0.111 * min_speed * 6) |
    #     """
    #     # get the keys and figure out some stuff
    #     keys = list(legs.keys())  # which legs are we moving
    #     numSteps = len(legs[keys[0]])  # how many steps in the cycle
    #     numServos = len(legs[keys[0]][0])-1  # how many servos per leg, -1 because speed there
    #
    #     if self.last_move is None:
    #         # assume we just turned on and was in the sit position
    #         # need a better solution
    #         self.last_move = {
    #             0: legs[0][0],
    #             1: legs[1][0],
    #             2: legs[2][0],
    #             3: legs[3][0]
    #         }
    #
    #     # curr_move = {}
    #     # for each step in legs
    #     for step in range(numSteps):
    #         dprint("\nStep[{}]===============================================".format(step))
    #         data = []
    #
    #         max_wait = 0
    #         # for legNum in [0,3,1,2]:
    #         for legNum in keys:
    #             dprint("  leg[{}]--------------".format(legNum))
    #             leg_angles_speed = legs[legNum][step]
    #             # print(leg_angles_speed)
    #             angles = leg_angles_speed[:4]
    #             speed = leg_angles_speed[4]
    #             sl, sh = le(speed)
    #
    #             # max_wait = 0
    #             for i, angle in enumerate(angles):
    #                 al, ah = angle2int(angle)  # angle
    #                 dprint("    Servo[{}], angle: {:.2f}, speed: {}".format(legNum*numServos + i+1, angle, speed))
    #                 data.append([legNum*numServos + i+1, al, ah, sl, sh])  # ID, low angle, high angle, low speed, high speed
    #
    #                 # print(self.last_move)
    #                 # print(leg_angles_speed)
    #                 # print(angles)
    #                 # print(i)
    #                 # print(legNum*numServos + i+1)
    #
    #                 oldangle = self.last_move[legNum][i]
    #                 # calculate wait time for a leg, take max time
    #                 w = abs((angle - oldangle)/(0.111*speed*6))
    #                 # print(angle - oldangle)
    #                 # print('w',w)
    #                 w *= 1.10  # scaling to make things look better: 1.3
    #                 max_wait = w if w > max_wait else max_wait
    #
    #             self.last_move[legNum] = leg_angles_speed
    #
    #         pkt = self.packet.makeSyncWritePacket(self.packet.base.GOAL_POSITION, data)
    #         self.serial.write(pkt)
    #         dprint("sent serial packet leg: {}".format(legNum))
    #         data = []
    #         print('max_wait', max_wait)
    #         time.sleep(max_wait)

    # def moveLegsGait4(self, legs):
    #     """
    #     gait or sequence?
    #     speed = 1 - 1023 (scalar, all servos move at same rate)
    #     {      step 0          step 1         ...
    #         0: [(t1,t2,t3,t4,speed), (t1,t2,t3,t4,speed), ...] # leg0
    #         2: [(t1,t2,t3,t4,speed), (t1,t2,t3,t4,speed), ...] # leg2
    #         ...
    #     } where t=theta
    #     NOTE: each leg needs the same number of steps and servos per leg
    #     WARNING: these angles are in servo space [0-300 deg]
    #
    #     [Join Mode]
    #     0 ~ 1,023(0x3FF) can be used, and the unit is about 0.111rpm.
    #     If it is set to 0, it means the maximum rpm of the motor is used
    #     without controlling the speed. If it is 1023, it is about 114rpm.
    #     For example, if it is set to 300, it is about 33.3 rpm.
    #
    #     AX12 max rmp is 59 (max speed 532)
    #     rev  min     360 deg      deg
    #     --- -------  ------- = 6 ----
    #     min  60 sec    rev        sec
    #
    #     sleep time = | (new_angle - old_angle) /(0.111 * min_speed * 6) |
    #     """
    #     # get the keys and figure out some stuff
    #     keys = list(legs.keys())  # which legs are we moving
    #     numSteps = len(legs[keys[0]])  # how many steps in the cycle
    #     numServos = len(legs[keys[0]][0])-1  # how many servos per leg, -1 because speed there
    #
    #     # if self.last_move is None:
    #     #     # assume we just turned on and was in the sit position
    #     #     # need a better solution
    #     #     self.last_move = {
    #     #         0: legs[0][0],
    #     #         1: legs[1][0],
    #     #         2: legs[2][0],
    #     #         3: legs[3][0]
    #     #     }
    #
    #     # curr_move = {}
    #     # for each step in legs
    #     for step in range(numSteps):
    #         # dprint("\nStep[{}]===============================================".format(step))
    #         data = []
    #
    #         # find max time we have to wait for all 4 legs to reach their end
    #         # point.
    #         max_wait = 0
    #         for legNum in keys:
    #             angles = legs[legNum][step][:4]
    #             speed = legs[legNum][step][4]
    #             # print(" speed", speed)
    #             for a, oa in zip(angles, self.last_move[legNum][:4]):
    #                 da = abs(a-oa)
    #                 w = calc_wait(da, speed)
    #                 # print(" calc_wait: {:.3f}".format(w))
    #                 # print("calc_wait: {}".format(w))
    #                 max_wait = w if w > max_wait else max_wait
    #
    #         # print(">> found wait", max_wait, " speed:", speed)
    #
    #         servo_speeds = [100,125,150,200]
    #
    #         # for legNum in [0,3,1,2]:
    #         for legNum in keys:
    #             # dprint("  leg[{}]--------------".format(legNum))
    #             leg_angles_speed = legs[legNum][step]
    #             # print(leg_angles_speed)
    #             angles = leg_angles_speed[:4]  # 4 servo angles
    #             speed = leg_angles_speed[4]
    #             # print("Speed:", speed, "wait", max_wait)
    #
    #             for i, angle in enumerate(angles):
    #                 # oldangle = self.last_move[legNum][i]
    #                 # due to rounding errors, to ensure the other servers finish
    #                 # BEFORE time.sleep(max_wait) ends, the the function it
    #                 # has less time
    #                 # spd = calc_rpm((angle - oldangle), 0.9*max_wait)
    #                 # now that i am scaling the spd parameter above, I sometimes
    #                 # exceed the original speed number, so saturate it if
    #                 # necessary
    #                 # spd = spd if spd <= speed else speed
    #                 # sl, sh = le(spd)
    #                 sl, sh = le(servo_speeds[i])
    #                 al, ah = angle2int(angle)  # angle
    #                 data.append([legNum*numServos + i+1, al, ah, sl, sh])  # ID, low angle, high angle, low speed, high speed
    #                 # data.append([legNum*numServos + i+1, al, ah])  # ID, low angle, high angle, low speed, high speed
    #
    #             self.last_move[legNum] = leg_angles_speed
    #
    #         pkt = self.packet.makeSyncWritePacket(self.packet.base.GOAL_POSITION, data)
    #         self.serial.write(pkt)
    #         dprint("sent serial packet leg: {}".format(legNum))
    #         data = []
    #         print('max_wait', max_wait)
    #         time.sleep(max_wait)
    #
    #         # time.sleep(1)


    # def moveLegsAnglesArray(self, angles, speed=None, degrees=True):
    #     """
    #     The ID number is set by the array position
    #     speed = 1 - 1023 (scalar, all servos move at same rate)
    #     angles = [servo1, servo2, servo3 ...]
    #     WARNING: these angles are in servo space [0-300 deg]
    #     """
    #     # print('legs', legs, '\n\n')
    #     # build sync message
    #     data = []
    #     if speed:
    #         sl, sh = le(speed)
    #     for i, a in enumerate(angles):
    #         a, b = angle2int(a)
    #         if speed:
    #             data.append([i+1, a, b, sl, sh])
    #         else:
    #             data.append([i+1, a, b])
    #     print('data', data)
    #     pkt = self.packet.makeSyncWritePacket(self.packet.base.GOAL_POSITION, data)
    #
    #     # Status Packet will not be returned if Broadcast ID(0xFE) is used
    #     self.serial.write(pkt)  # no point to read
    #     # self.serial.sendPkt(pkt)
    #     print('moveLegsAnglesArray', pkt)

    # def stand(self):
    #     if self.positions['stand']:
    #         feet = {
    #             0: [self.positions['stand']],
    #             1: [self.positions['stand']],
    #             2: [self.positions['stand']],
    #             3: [self.positions['stand']],
    #         }
    #         self.moveLegsGait(feet, 100)
    #         sleep(4)
    #
    # def sit(self):
    #     if self.positions['sit']:
    #         feet = {
    #             0: [self.positions['sit']],
    #             1: [self.positions['sit']],
    #             2: [self.positions['sit']],
    #             3: [self.positions['sit']],
    #         }
    #         self.moveLegsGait(feet, 100)
    #         sleep(4)
    # def moveLegsPosition2(self, legs):
    #     """
    #     this only does position
    #     [   step 0          step 1         ...
    #         [[t1,t2,t3,t4], [t1,t2,t3,t4], ...] # leg0
    #         [[t1,t2,t3,t4], [t1,t2,t3,t4], ...] # leg1
    #         ...
    #     ]
    #
    #     FIXME: don't hard code for 4 legs, might want to just move 1 or 2 or 3
    #     """
    #     # print('legs', legs, '\n\n')
    #     # build sync message
    #     # FIXME: hard coded for 4 legs
    #     for j, step in enumerate(zip(*legs)):  # servo angles for each leg at each step
    #         data = []  # [id, lo, hi, id, lo, hi, ...]
    #         # leg 0: 0 1 2 3
    #         # print('step', len(step), step, '\n')
    #         self.pprint(j, step)
    #         for i, leg in enumerate(step):  # step = [leg0, leg1, leg2, leg3]
    #             # print('leg', len(leg), leg)
    #             for j, servo in enumerate(leg):  # leg = [servo0, servo1, servo2, servo3]
    #                 s = []
    #                 s.append(4*i+j)      # servo ID
    #                 a, b = angle2int(servo)  # angle
    #                 s.append(a)
    #                 s.append(b)
    #                 data.append(s)
    #
    #         # print('\n\ndata', data)
    #
    #         pkt = self.packet.makeSyncWritePacket(self.packet.base.GOAL_POSITION, data)
    #         self.serial.sendPkt(pkt)

    # def moveLegsPosition(self, legs):
    #     """
    #     [   step 0          step 1         ...
    #         [[t1,t2,t3,t4], [t1,t2,t3,t4], ...] # leg0
    #         [[t1,t2,t3,t4], [t1,t2,t3,t4], ...] # leg1
    #         ...
    #     ]
    #
    #     FIXME: this moves angles from a gait, not position (x,y,z) ... rename or change interface to take points?
    #     FIXME: don't hard code for 4 legs, might want to just move 1 or 2 or 3
    #     FIXME: legs are positional ... can't just move leg 3, try:
    #         legs = { here legs 1 and 4 are not moved
    #             0: [t1,t2, ...], ... move leg 0
    #             3: [t1, t2 ...], ... move leg 3
    #         }
    #     """
    #     # print('legs', legs, '\n\n')
    #     # build sync message
    #     # FIXME: hard coded for 4 legs
    #     for g, step in enumerate(zip(*legs)):  # servo angles for each leg at each step
    #         data = []  # [id, lo, hi, id, lo, hi, ...]
    #         # leg 0: 0 1 2 3
    #         # print('step', len(step), step, '\n')
    #         self.pprint(g, step)
    #         num_legs = len(step)
    #         for i, leg in enumerate(step):  # step = [leg0, leg1, leg2, leg3]
    #             # print('leg', len(leg), leg)
    #             num_joints = len(leg)
    #             for j, servo in enumerate(leg):  # leg = [servo0, servo1, servo2, servo3]
    #                 s = []
    #                 s.append(num_joints*i+j)      # servo ID
    #                 a, b = angle2int(servo)  # angle
    #                 s.append(a)
    #                 s.append(b)
    #                 data.append(s)
    #
    #         # print('\n\ndata', data)
    #
    #         pkt = self.packet.makeSyncWritePacket(self.packet.base.GOAL_POSITION, data)
    #         self.serial.sendPkt(pkt)

    # # FIXME: this also applies to non-gait movement ... moveLegs???
    # def moveLegsGait(self, legs, speed=None):
    #     """
    #     gait or sequence?
    #     speed = 1 - 1023 (scalar, all servos move at same rate)
    #     legs = { step 0        step 1         ...
    #         0: [[t1,t2,t3,t4], [t1,t2,t3,t4], ...] # leg0
    #         1: [[t1,t2,t3,t4], [t1,t2,t3,t4], ...] # leg1
    #         3: [[servo1, servo2, ...]] angles in servo space [0-300] deg
    #     }
    #     NOTE: each leg needs the same number of steps and servos per leg
    #     WARNING: these angles are in servo space [0-300 deg]
    #     """
    #     # get the keys and figure out some stuff
    #     keys = list(legs.keys())
    #     numSteps = len(legs[keys[0]])
    #     numServos = len(legs[keys[0]][0])
    #     wait = self.wait  # FIXME: wait should be a function of speed
    #
    #     # print("Speed: {} =====================".format(speed))
    #
    #     def ramp(val, length):
    #         """
    #         Simple triangle for scaling speed. it always returns 0.5 at the lowest
    #         and is 1.0 at max in the middle
    #
    #         in: val - step
    #             length - number of steps
    #         out: 0.5 - 1.0
    #         """
    #         val = val % length
    #         # print("ramp: {} {} {}".format(val, length/2, length))
    #         slope = 0.5/(length/2)
    #         if val > length/2:
    #             # since it is symetric, just mirror the answer
    #             val = (length - val)
    #         return slope*val + 0.5
    #
    #     # for each step in legs
    #     for s in range(numSteps):
    #         data = []
    #         for legNum in keys:
    #             step = legs[legNum][s]
    #             for i, a in enumerate(step):
    #                 a, b = angle2int(a)  # angle
    #
    #                 # remember, servo IDs start at 1 not 0, so there is a +1
    #                 if speed:
    #                     scale = ramp(s, 12)
    #                     sl, sh = le(int(scale*speed))
    #                     # print("LegNum[{}] Servo[{}] step: {}, scale: {:.2f}, speed: {}".format(legNum, legNum*numServos + i+1, s, scale, int(scale*speed)))
    #                     data.append([legNum*numServos + i+1, a, b, sl, sh])  # ID, low angle, high angle, low speed, high speed
    #                 else:
    #                     dspeed = 100
    #                     sl, sh = le(dspeed)
    #                     # print("LegNum[{}] Servo[{}] step: {}, speed: {}".format(legNum, legNum*numServos + i+1, s, dspeed))
    #                     data.append([legNum*numServos + i+1, a, b, sl, sh])  # ID, low angle, high angle
    #
    #         # print('\n\ndata', data)
    #
    #         pkt = self.packet.makeSyncWritePacket(self.packet.base.GOAL_POSITION, data)
    #         # print('raw pkt', pkt)
    #         self.serial.write(pkt)
    #         time.sleep(wait)
    #         # print('moveLegsGait', wait)
