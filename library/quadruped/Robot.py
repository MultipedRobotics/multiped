#!/usr/bin/env python

##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################
# Simple robot that you can drive with a PS4 joystick
#
# It is meant to run on a raspberry pi and if linux isn't detected, then some
# sensors are not loaded.

from __future__ import print_function
from __future__ import division
from quadruped import Engine
from quadruped import DiscreteRippleGait
# import platform
# import time
##########################


class Robot(object):
	"""
	This is a simple class that binds the others together. You could make it
	a base class for something fancier.
	"""
	def __init__(self, data, gaits=None):
		"""
		Constructor.
		Engine - commands the leg servos to move
		gait - Ideally there are several types of gaits for different
				walking/running situations. If you don't give it an dict
				of gaits, then the default is just the standard
				DiscreteRippleGait.
			The gaits need to know:
			- how high to pick up a leg
			- what the neutral leg position is (where is the foot
				located when just standing?)
		"""
		self.robot = Engine(data)
		neutral = self.robot.getFoot0(0)

		if gaits is None:
			self.gait = {
				'crawl': DiscreteRippleGait(45.0, neutral)
			}
		else:
			self.gait = gaits
