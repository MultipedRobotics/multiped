from __future__ import print_function
from __future__ import division
from .Engine import Engine
from .Gait import DiscreteRippleGait
# from .Leg3 import Leg3, LegException
from quadruped.kinematics4 import Kinematics4
# from .Servo import Servo  # don't need
from .Robot import Robot

# do I put exceptions here?

# gait - servo positions for one cycle
# engine - talk to servos/packet/bulk/sync
# servo - individual parameters for each servo
# leg - fk/ik
# robot - one of each above

__author__ = 'Kevin J. Walchko'
__license__ = 'MIT'
__version__ = '0.5.0'
