#!/usr/bin/env python

##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################
# Simple robot

from __future__ import print_function
from __future__ import division
from multiped import Engine
from multiped import DiscreteRippleGait
# import time
##########################


class Robot(object):
	"""
	This is a simple class that binds the others together. You could make it
	a base class for something fancier.
	"""
	def __init__(self, data, legType, servoType):
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
		self.engine = Engine(data, servoType)
		self.kinematics = legType(data)

		neutral = self.kinematics.getNeutralPos()

		if 'gaits' in data:
			self.gaits = data['gaits']
		else:
			self.gaits = {
				'crawl': DiscreteRippleGait(65.0, neutral)
			}
