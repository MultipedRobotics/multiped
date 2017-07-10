#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
from nose.tools import raises
import sys
# sys.path.insert(0, '..')
from quadruped.Servo import Servo
# from pyxl320 import DummySerial


def test_limits():
	s = Servo(15)
	s.setServoLimits(0, 0, 180)
	s.angle = 0; assert(s.angle == 0)
	s.angle = 45; assert(s.angle == 45)
	s.angle = 90; assert(s.angle == 90)
	s.angle = 180; assert(s.angle == 180)
	s.angle = 270; assert(s.angle == 180), "{}".format(s.angle)
	s.angle = -45; assert(s.angle == 0)
	s.angle = -90; assert(s.angle == 0)
	s.angle = -270; assert(s.angle == 0)

	s.setServoLimits(150, -90, 90)
	s.angle = 0; assert(s.angle == 0)
	s.angle = 45; assert(s.angle == 45)
	s.angle = 90; assert(s.angle == 90)
	s.angle = 180; assert(s.angle == 90)
	s.angle = 270; assert(s.angle == 90)
	s.angle = -45; assert(s.angle == -45)
	s.angle = -90; assert(s.angle == -90)
	s.angle = -270; assert(s.angle == -90)


@raises(Exception)
def test_fail2():
	s = Servo(15)
	s.setServoLimits(0, 180, 0)  # min > max ... error

# def checks():
# 	check = lambda x, a, b: max(min(b, x), a)
# 	print('0 in [0,180]:', check(0, 0, 180))
# 	print('90 in [0,180]:', check(90, 0, 180))
# 	print('180 in [0,180]:', check(180, 0, 180))
# 	print('-90 in [0,180]:', check(-90, 0, 180))
# 	print('-180 in [0,180]:', check(-180, 0, 180))
# 	print('--------------------')
# 	print('these are wrong! Cannot reverse order')
# 	print('0 in [180,0]:', check(0, 180, 0))
# 	print('45 in [180,0]:', check(45, 180, 0))
# 	print('90 in [180,0]:', check(90, 180, 0))
# 	print('180 in [180,0]:', check(180, 180, 0))
# 	print('-90 in [180,0]:', check(-90, 180, 0))
# 	print('-180 in [180,0]:', check(-180, 180, 0))
# 	print('--------------------')
# 	print('0 in [-180,0]:', check(0, -180, 0))
# 	print('90 in [-180,0]:', check(90, -180, 0))
# 	print('180 in [-180,0]:', check(180, -180, 0))
# 	print('-90 in [-180,0]:', check(-90, -180, 0))
# 	print('-45 in [-180,0]:', check(-45, -180, 0))
# 	print('-180 in [-180,0]:', check(-180, -180, 0))


if __name__ == "__main__":
	print('run this with "nosetests -v test_servo.py"')
