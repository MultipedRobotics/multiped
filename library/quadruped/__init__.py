from __future__ import print_function
from __future__ import division
from quadruped.Engine import Engine
from quadruped.Gait import DiscreteRippleGait
# from quadruped.kinematics3 import Kinematics3
from quadruped.kinematics4 import Kinematics4
# from .Servo import Servo  # don't need
from quadruped.Robot import Robot

# do I put exceptions here?

# gait - generates 3d (x,y,z) points for one cycle
# engine - talk to servos/packet/bulk/sync
# servo - individual parameters for each servo
# kinematics - fk/ik
# robot - holds above along with other logic and sensors

__author__ = 'Kevin J. Walchko'
__license__ = 'MIT'
__version__ = '0.5.0'
