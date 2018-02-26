#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
from quadruped import Engine
from quadruped import DiscreteRippleGait
# from quadruped import Robot
# from misc_gaits import CircularGait, ImpatientGait
from math import pi
import time


# length: how long is the link
# limits: min/max limits so we don't hit something
# offset: match servo frame and DH frame up
data = {    # [ length, (limits), offset]
	'coxa': [28, [-45,45], 150],
	'femur': [90, [-90,90], 150],
	'tibia': [84, [-90,90], 150],
	'tarsus': [98, [-90,90], 150],
	'stand': [0, -110, -40, 90],
	'sit': [0,90,90,90]
}

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
