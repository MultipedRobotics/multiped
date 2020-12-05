##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from math import cos, sin, sqrt, pi
from multiped.utils import constrain, Rz
import numpy as np


class TripodGait:
    case = (1,2,1,2,1,2)
    home = np.array([60,0,-50])
    body = (0,0,0)

    def compute_strides(self,commandedX,commandedY,commandedZ, commandedR):
        # compute stride lengths
        self.strideX = 90*commandedX
        self.strideY = 90*commandedY
        self.strideR = pi/4*commandedR  # was 35

        # compute rotation trig
        self.sinRotZ = sin(self.strideR)
        self.cosRotZ = cos(self.strideR)

        # print(f">> stride: {self.strideX} {self.strideY} {self.strideR}")
        # print(f">> rot: {self.sinRotZ} {self.cosRotZ}\n")

    def compute_amplitudes(self):
        # compute total distance from center of body to toe
        totalX = self.home[0] + self.body[0]
        totalY = self.home[1] + self.body[1]

        # compute rotational offset
        rotOffsetX = totalY*self.sinRotZ + totalX*self.cosRotZ - totalX
        rotOffsetY = totalY*self.cosRotZ - totalX*self.sinRotZ - totalY

        # compute X and Y amplitude and constrain to prevent legs from crashing into each other
        amplitudeX = (self.strideX + rotOffsetX)/2.0
        amplitudeY = (self.strideY + rotOffsetY)/2.0
        amplitudeX = constrain(amplitudeX,-50,50)
        amplitudeY = constrain(amplitudeY,-50,50)

        # compute Z amplitude
        step_height_multiplier = 1.0
        if (abs(self.strideX + rotOffsetX) > abs(self.strideY + rotOffsetY)):
            amplitudeZ = step_height_multiplier * (self.strideX + rotOffsetX) / 4.0
        else:
            amplitudeZ = step_height_multiplier * (self.strideY + rotOffsetY) / 4.0

        return amplitudeX,amplitudeY,amplitudeZ

    def command(self, commandedX, commandedY, commandedZ, commandedR):
        """
        Given a command, this returns an array of movments for one cycle

        return:
        feet = {
            0: [(x0,y0,z0), (x1,y1,z1), ... (xn,yn,zn)] # leg0, all foot locations for one cycle
            1: [...]
            ...
            5: [...]
        }
        """
        min_cmd = 0.1
        if((abs(commandedX) < min_cmd) or (abs(commandedY) < min_cmd) and (abs(commandedR) > 360)):
            return None

        feet = {
            0: [], 1: [], 2: [], 3: [], 4: [], 5: [],
        }

        case = ((1,2,1,2,1,2),(2,1,2,1,2,1))

        for s in (0,1):
            self.case = case[s]
            max_step = 12
            for i in range(max_step):
                steps = self.one_time_step(commandedX, commandedY, commandedZ, commandedR, i/max_step)
                for leg in range(6):
                    feet[leg].append(steps[leg])

        # print(f">> feet0: {feet[0]}")
        return feet


    def one_time_step(self, commandedX, commandedY, commandedZ, commandedR, dstep):
        # print(f">> step: {dstep}")
        ret = [0]*6
        self.compute_strides(commandedX, commandedY, commandedZ, commandedR)
        amplitudeX,amplitudeY,amplitudeZ = self.compute_amplitudes()
        # print(f">> Amp: {amplitudeX} {amplitudeY} {amplitudeZ}")
        # numTicks = int(duration / FRAME_TIME_MS / 2.0) # total ticks divided into the two cases
        # rot = [-pi/6, -pi/2, -5*pi/6,5*pi/6, pi/2, pi/6]
        rot = [-pi/6, -pi/2, -5*pi/6, 5*pi/6+pi, pi/2+pi, pi/6+pi]
        for leg_num in [0,1,2,3,4,5]:
            # amplitudeX,amplitudeY,amplitudeZ = self.compute_amplitudes()
            # print(f">> Amp: {amplitudeX} {amplitudeY} {amplitudeZ}")
            if self.case[leg_num] == 1:  # move foot forward (raise and lower)
                # ret[leg_num] = [0,0,0]
                # ret[leg_num][0] = self.home[0] - amplitudeX*cos(pi*dstep)
                # ret[leg_num][1] = self.home[1] - amplitudeY*cos(pi*dstep)
                # ret[leg_num][2] = self.home[2] + abs(amplitudeZ)*sin(pi*dstep)
                # if (dstep >= 1.0):
                #     self.case[leg_num] = 2
                angle = rot[leg_num]
                R = Rz(angle)
                m = np.array([
                    - amplitudeX*cos(pi*dstep),
                    - amplitudeY*cos(pi*dstep),
                    abs(amplitudeZ)*sin(pi*dstep)
                ])
                ft = R @ (self.home + m)
                ret[leg_num] = ft

            elif self.case[leg_num] == 2:  # move foot back (on the ground)
                # ret[leg_num] = [0,0,0]
                # ret[leg_num][0] = self.home[0] + amplitudeX*cos(pi*dstep)
                # ret[leg_num][1] = self.home[1] + amplitudeY*cos(pi*dstep)
                # ret[leg_num][2] = self.home[2]
                # if (dstep >= 1.0):
                #     self.case[leg_num] = 1
                angle = rot[leg_num]
                R = Rz(angle)
                m = np.array([
                    + amplitudeX*cos(pi*dstep),
                    + amplitudeY*cos(pi*dstep),
                    0
                ])
                ft = R @ (self.home + m)
                ret[leg_num] = ft

        # print(f">> feet: {ret}")
        return ret
























































# debug = False
#
#
# def rot_z_tuple(t, c):
#     """
#     t - theta [radians]
#     c - [x,y,z]
#     return - (x,y,z) tuple rotated about z-axis
#     """
#     ans = (
#         c[0]*cos(t)-c[1]*sin(t),
#         c[0]*sin(t)+c[1]*cos(t),
#         c[2]
#     )
#
#     return ans
#
#
# # make a static method in Gait? Nothing else uses it
# def rot_z(t, c):
#     """
#     t - theta [radians]
#     c - [x,y,z]
#     return - [x,y,z] numpy array rotated about z-axis
#     """
#     ans = [
#         c[0]*cos(t)-c[1]*sin(t),
#         c[0]*sin(t)+c[1]*cos(t),
#         c[2]
#     ]
#
#     return ans

# class Tripod:
#     def __init__(self, neutral, forward, back, count):
#         self.build_forward()
#
#     def build_forward(self, n,f,b, c):
#

    # @classmethod
    # def from_params(cls, neutral, forward, back):
    #     tri = cls()
    #
    #     return tri


# class Gait(object):
#     """
#     Base class for gaits. Gait only plan all foot locations for 1 complete cycle
#     of the gait.
#
#     Like to add center of mass (CM) compensation, so we know the CM is always
#     inside the stability triangle.
#
#     Gait knows:
#     - how many legs
#     - leg stride (neutral position)
#     """
#     # these are the offsets of each leg
#     legOffset = [0, 6, 3, 9]
#     # frame rotations for each leg
#     # cmrot = [pi/4, -pi/4, -3*pi/4, 3*pi/4]
#     # frame = [-pi/4, pi/4, 3*pi/4, -3*pi/4]  # this seem to work better ... wtf?
#     frame = [pi/4, -pi/4, -3*pi/4, 3*pi/4]
#     moveFoot = None
#     rest = None
#     scale = 50.0
#
#     def __init__(self, rest):
#         # the resting or idle position/orientation of a leg
#         self.rest = rest
#
#     def command(self, cmd):
#         """
#         Send a command to the quadruped
#         cmd: [x, y, rotation about z-axis], the x,y is a unit vector and
#         rotation is in radians
#         """
#         x, y, rz = cmd
#         d = sqrt(x**2+y**2)
#
#         # handle no movement command ... do else where?
#         if d <= 0.1 and abs(rz) < 0.1:
#             x = y = 0.0
#             rz = 0.0
#             return None
#         # commands should be unit length, oneCyle scales it
#         elif 0.1 < d:
#             x /= d
#             y /= d
#         else:
#             return None
#
#         angle_limit = pi/2
#         if rz > angle_limit:
#             rz = angle_limit
#         elif rz < -angle_limit:
#             rz = -angle_limit
#
#         return self.oneCycle_alt(x, y, rz)
#
#     def oneCycle_alt(self, x, y, rz):
#         raise NotImplementedError('*** Gait: wrong function, this is base class! ***')
#
#
# class DiscreteRippleGait(Gait):
#     """
#     Discrete 12 step gait
#     """
#     steps = 0
#
#     def __init__(self, height, rest):
#         """
#         height: added to z
#         rest: the neutral foot position
#         """
#         Gait.__init__(self, rest)
#         # self.phi = [8/8, 7/8, 1/8, 0/8, 1/8, 2/8, 3/8, 4/8, 5/8, 6/8, 7/8, 8/8]
#         self.phi = [10/10, 5/10, 0/10, 1/10, 2/10, 3/10, 4/10, 5/10, 6/10, 7/10, 8/10, 9/10]
#         self.setLegLift(height)
#         self.steps = len(self.phi)
#
#     def setLegLift(self, lift):
#         # legs lift in the sequence: 0, 3, 1, 2
#         #           0     1     2    3    4    5    6    7    8    9   10   11
#         self.z = [0.0, lift, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # leg height
#
#     def eachLeg(self, index, cmd):
#         """
#         interpolates the foot position of each leg
#         cmd:
#             linear (mm)
#             angle (rads)
#         """
#         rest = self.rest
#         i = index
#         phi = self.phi[i]
#         xx, yy, rzz = cmd
#
#         # rotational commands -----------------------------------------------
#         angle = rzz/2-rzz*phi
#         rest_rot = rot_z(-angle, rest)
#
#         # create new move command
#         move = [
#             xx/2 - phi*xx,
#             yy/2 - phi*yy,
#             self.z[i]
#         ]
#
#         # new foot position: newpos = rot + move ----------------------------
#         # newpos = linear_movement + angular_movement
#         # newpos = move + rest_rot
#         newpos = [0, 0, 0]
#         newpos[0] = move[0] + rest_rot[0]
#         newpos[1] = move[1] + rest_rot[1]
#         newpos[2] = move[2] + rest_rot[2]
#
#         # print('New  [](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(newpos[0], newpos[1], newpos[2]))
#         return newpos
#
#     def move_cg(self, leg, off, pt, leg_lift):
#         """
#         There is a pattern of which direction to shift based on which leg you
#         are trying to move and which leg is lifted (not currently providing
#         support for the robot)
#         leg - leg number
#         off - offset in mm to shift cm
#         leg_lift - which leg is moving through the air currently
#
#         lift 0: x-d    1: y-d    2: x+d    3: y+d
#                 y+d       x-d       y-d       x+d
#                 x+d       y+d       x-d       y-d
#                 y-d       x+d       y+d       x-d
#         pattern: always x y x y (alternate)
#                  always - + + -
#         """
#         axis = [0, 1, 0, 1]  # 0=x, 1=y componets of 3d point
#         offset = [-off, off, off, -off]  # either adding or subtracting offset from point
#         ia = axis[(leg+leg_lift) % 4]  # us mod to rotate through each of these indexes
#         io = (leg-leg_lift) % 4
#         pt[ia] += offset[io]  # shift point
#         return pt
#         # if leg == 0:
#         #     if   leg_lift == 0: pt[0] -= offset  # x-d
#         #     elif leg_lift == 1: pt[1] += offset  # y+d
#         #     elif leg_lift == 2: pt[0] += offset  # x+d
#         #     elif leg_lift == 3: pt[1] -= offset  # y-d
#         # elif leg == 0:
#         #     if   leg_lift == 0: pt[1] -= offset  # x-d
#         #     elif leg_lift == 1: pt[0] -= offset  # y+d
#         #     elif leg_lift == 2: pt[1] += offset  # x+d
#         #     elif leg_lift == 3: pt[0] += offset  # y-d
#
#
#     def oneCycle(self, x, y, rz):
#         """
#         direction of travel x, y (2D plane) or rotation about z-axis
#         Returns 1 complete cycle for all 4 feet (x,y,z)
#         """
#
#         # check if x, y, rz is same as last time commanded, if so, return
#         # the last cycle response, else, calculate a new response
#         # ???
#
#         scale = self.scale
#         cmd = (scale*x, scale*y, rz)
#         ret = {
#             0: [],
#             1: [],
#             2: [],
#             3: []
#         }  # 4 leg foot positions for the entire 12 count cycle is returned
#
#         # iteration, there are 12 steps in gait cycle, add a 13th so all feet
#         # are on the ground at the end, otherwise one foot is still in the air
#         leg_lift = [0,0,0,3,3,3,1,1,1,2,2,2]
#         for i in range(0, self.steps):
#             for legNum in [0, 1, 2, 3]:  # order them diagonally
#                 rcmd = rot_z_tuple(self.frame[legNum], cmd)
#                 index = (i + self.legOffset[legNum]) % self.steps
#                 pos = self.eachLeg(index, rcmd)  # move each leg appropriately
#                 # print('Foot[{}]: {:.2f} {:.2f} {:.2f}'.format(legNum, *(pos)))
#
#                 # shift cg
#                 # fist and last shouldn't move cg??
#                 # pos = self.move_cg(legNum, 40, pos, leg_lift[i])
#
#                 ret[legNum].append(pos)
#
#         if debug:
#             print("=[Gait.py]===============================")
#             for legNum in [0, 1, 2, 3]:
#                 print('Leg[{}]---------'.format(legNum))
#                 for i, pt in enumerate(ret[legNum]):
#                     print('  {:2}: {:7.2f} {:7.2f} {:7.2f}'.format(i, *pt))
#
#         return ret


    # def oneCycle2(self, x, y, rz):
    #     """
    #     direction of travel x, y (2D plane) or rotation about z-axis
    #     Returns 1 complete cycle for all 4 feet (x,y,z)
    #     """
    #
    #     # check if x, y, rz is same as last time commanded, if so, return
    #     # the last cycle response, else, calculate a new response
    #     # ???
    #
    #     scale = self.scale
    #     cmd = (scale*x, scale*y, rz)
    #     ret = {
    #         0: [],
    #         1: [],
    #         2: [],
    #         3: []
    #     }  # 4 leg foot positions for the entire 12 count cycle is returned
    #
    #     # iteration, there are 12 steps in gait cycle, add a 13th so all feet
    #     # are on the ground at the end, otherwise one foot is still in the air
    #     leg_lift = [0,0,0,3,3,3,1,1,1,2,2,2]
    #     for i in range(0, self.steps)+[0]:
    #         for legNum in [0, 1, 2, 3]:  # order them diagonally
    #             rcmd = rot_z_tuple(self.frame[legNum], cmd)
    #             index = (i + self.legOffset[legNum]) % self.steps
    #             pos = self.eachLeg(index, rcmd)  # move each leg appropriately
    #             # print('Foot[{}]: {:.2f} {:.2f} {:.2f}'.format(legNum, *(pos)))
    #
    #             # shift cg
    #             # fist and last shouldn't move cg??
    #             pos = self.move_cg(legNum, 40, pos, leg_lift[i])
    #
    #             ret[legNum].append(pos)
    #
    #     if debug:
    #         for legNum in [0, 1, 2, 3]:
    #             print('Leg[{}]---------'.format(legNum))
    #             for i, pt in enumerate(ret[legNum]):
    #                 print('  {:2}: {:7.2f} {:7.2f} {:7.2f}'.format(i, *pt))
    #
    #     return ret

    # def oneCycle_alt2(self, x, y, rz):
    #     """
    #     direction of travel x, y (2D plane) or rotation about z-axis
    #     Returns 1 complete cycle for all 4 feet (x,y,z)
    #     """
    #
    #     # check if x, y, rz is same as last time commanded, if so, return
    #     # the last cycle response, else, calculate a new response
    #     # ???
    #
    #     scale = self.scale
    #     cmd = (scale*x, scale*y, rz)
    #     ret = {
    #         0: [],
    #         1: [],
    #         2: [],
    #         3: []
    #     }  # 4 leg foot positions for the entire 12 count cycle is returned
    #
    #     speed = 100
    #
    #     # iteration, there are 12 steps in gait cycle, add a 13th so all feet
    #     # are on the ground at the end, otherwise one foot is still in the air
    #     for i in range(0, self.steps)+[0]:
    #         for legNum in [0, 1, 2, 3]:  # order them diagonally
    #             rcmd = rot_z_tuple(self.frame[legNum], cmd)
    #             index = (i + self.legOffset[legNum]) % self.steps
    #             pos = self.eachLeg(index, rcmd)  # move each leg appropriately
    #             # print('Foot[{}]: {:.2f} {:.2f} {:.2f}'.format(legNum, *(pos)))
    #             ret[legNum].append((pos, speed,))
    #
    #     for legNum in [0, 1, 2, 3]:
    #         print('Leg[{}]---------'.format(legNum))
    #         for i, pt in enumerate(ret[legNum]):
    #             print('  {}:'.format(i), pt)
    #
    #     return ret
