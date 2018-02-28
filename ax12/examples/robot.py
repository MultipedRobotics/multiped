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
from quadruped import Robot
from quadruped import Leg4
# from misc_gaits import CircularGait, ImpatientGait
from math import pi
import time


class Test(Robot):
	def __init__(self, data, gaits=None):
		Robot.__init__(self, data, Leg4, gaits)

	def run(self):
		# predefined walking path
		# x, y, rotation
		path = [
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[0, 0, pi/4],
			[0, 0, pi/4],
			[0, 0, pi/4],
			[0, 0, -pi/4],
			[0, 0, -pi/4],
			[0, 0, -pi/4],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
		]

		# pick a gait to use
		crawl = self.gaits['crawl']
		# crawl = self.gaits['circle_tap']
		# crawl = self.gaits['impatient_tap']

		for cmd in path:

			print('***********************************')
			# print(' rest {:.2f} {:.2f} {:.2f}'.format(*leg))
			# print('ahrs[deg]: roll {:.2f} pitch: {:.2f} yaw: {:.2f}'.format(d[0], d[1], d[2]))
			print(' cmd {:.2f} {:.2f} {:.2f}'.format(*cmd))
			# print('***********************************')
			mov = crawl.command(cmd)  # take command and return 4 foot locations
			angles = self.kinematics.generateServoAngles(mov)
			self.engine.move(angles)


def main():
	# data = {
	# 	# 'serialPort': '/dev/tty.usbserial-AL034G2K',  # sparkfun usb-serial
	# 	'serialPort': '/dev/ttyUSB0',
	# 	'write': 'bulk'
	# }

	# gaits = {
	# 	'crawl': DiscreteRippleGait,
	# 	'circle_tap': CircularGait,
	# 	'impatient_tap': ImpatientGait
	# }

	# length: how long is the link
	# limits: min/max limits so we don't hit something
	# offset: match servo frame and DH frame up
	data = {
		# leg3/4
		# [ length, (limits), offset]
		'coxa': [28, [-45, 45], 150],
		'femur': [90, [-90, 90], 150],
		'tibia': [84, [-90, 90], 150],
		'tarsus': [98, [-90, 90], 150],

		# gait
		'stand': [0, -110, -40, 90],
		'sit': [0, 90, 90, 90],

		# engine
		'serialPort': '/dev/ttyUSB0',
		'write': 'bulk'
	}

	test = Test(data)

	try:
		test.run()
	except KeyboardInterrupt:
		print('bye ...')
		time.sleep(1)


if __name__ == '__main__':
	main()
