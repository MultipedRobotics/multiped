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
from pyservos import AX12
# import platform
# import time
##########################


class Robot(object):
	"""
	This is a simple class that binds the others together. You could make it
	a base class for something fancier.
	"""
	def __init__(self, data, legType, gaits=None):
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
		self.engine = Engine(data, AX12)

		# # angle offsets to line up with fk
		# for i in range(0, 4):  # 4 legs
		# 	channel = i*spl  # x servos per leg
		# 	if spl == 3:
		# 		self.legs.append(
		# 			Leg3([channel+1, channel+2, channel+3])
		# 		)
		# 	elif spl == 4:
		# 		self.legs.append(
		# 			Leg4([channel+1, channel+2, channel+3, channel+4])
		# 		)
		# 	else:
		# 		raise Exception('Robot() invalid number of servos per leg:', spl)

		self.kinematics = legType(data)

		neutral = self.kinematics.getNeutralPos()

		if gaits:
			self.gait = gaits
		else:
			self.gait = {
				'crawl': DiscreteRippleGait(45.0, neutral)
			}
