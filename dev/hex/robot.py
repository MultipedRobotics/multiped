#!/usr/bin/env python3

# from multiped import
from mdh.link import mdh_params, JointType
from mdh.kinematic_chain import KinematicChain

from multiped.gait import Tripod

from pyservos import AX12

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
