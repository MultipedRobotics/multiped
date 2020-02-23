#!/usr/bin/env python3

from mdh.link import mdh_params, JointType
from mdh.kinematic_chain import KinematicChain
from numpy import linspace
from math import pi, sin, cos
from collections import deque

# from pyservos import AX12

class Tripod:
    def __init__(self, neutral, stride, count):
        self.gait = self.build_forward(neutral, stride, count)
        self.orientations = [-30, -90, -120, 120, 90, 30]
        self.

    def build_stride(self, n, dist, steps):
        """
        Build a complete stride that starts at the origin (0,0,0) and ends
        there.

        Neutral: foot positions, [(x1,y1), (x2,y2), ...] where 1=Leg1, 2=Leg2, ...
        Distance [mm]: complete length the foot moves
        Steps: how many steps to take
        Returns: (phase(0), phase(90))
        """
        if steps % 4 != 0:
            raise Exception(f"Invalide number of steps: {steps}")
        half = steps//2 # half of teh steps to move to rear position
        mid = dist/2 # half of the steps to move forward to start position
        stride = []
        step = 2*mid/half # incremental distance of each step [mm]

        for i in range(half):
            stride.append([0,mid-step*i, 0])
        for i in range(half):
            a = pi - pi*i/half
            stride.append([0,(mid)*cos(a), mid*sin(a)])

        # now shift the step pattern to where we want and produce
        # 2 sets starting at the origin, but one is on the ground and the
        # other is raised up in the air
        s = deque(stride)
        s.rotate(half//2) # shift to start at origin (0,0,0)
        ss = deque(s)
        ss.rotate(half) # shift to start at origin (0,0,range)

        return (s, ss,)

    def build_forward(self, neutral, stride, steps):
        s, ss = self.build_stride(neutral, stride, steps)
        g = []
        for i, p in enumerate(self.orientations):
            st = s if i%2 else ss
            g.append(self.rotate_z(st, p, neutral[i]))
        return g

    def rotate_z(self, stride, angle, offset):
        ret = []
        for s in stride:
            # print(s, offset)
            x,y,z = s
            xx, yy = offset
            a = angle*pi/180
            r = [
                x*cos(a)-y*sin(a)+xx,
                x*sin(a) + y*cos(a)+yy,
                z
            ]
            ret.append(r)
        return ret

    def gait_world(self):
        ret = []
        for i in range(6):

        return ret

    def __getitem__(self, key):
        if isinstance(key, int) and (0 < key < 6):
            return self.gait[key]
        # elif isinstance(key, tuple):
        #     return self.gait[]
        else:
            raise Exception(f"Gait, invalide key: {key}")


class Robot:
    def __init__(self, params):
        self.kinematicChain = KinematicChain.from_parameters(params["mdh"])

        # interpolate walk, forward/back, using neutral, forward, back steps
        # and interpolating between them
        n = params["neutral"]
        fw = params["forward"]
        bk = params["back"]
        h = params["height"]
        self.gait = Tripod(h, n, fw, bk)

        num_legs = len(n)
        num_servos = len(self.kinematicChain)
        self.engine = Engine(num_legs, num_servos, AX12)

    def forward(self):
        pass

    def backwards(self):
        pass

    def turn(self, dir):
        pass

    def z(self, altitude):
        # altitude: 0 = sit, >0 = stand
        pass
