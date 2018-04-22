#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
from quadruped import Engine
# from quadruped import DiscreteRippleGait
from quadruped import Leg4
from pyservos import AX12
import time


class LegTest(object):
	def __init__(self):
		data = {
			# [ length, (limits), offset]
			'coxa':   [52, [-90, 90], 150],
			'femur':  [90, [-90, 90], 150],   # fixme
			'tibia':  [89, [-90, 120], 220],  # fixme
			'tarsus': [90, [-90, 90], 150],

			# gait
			# Angles: 0.00 75.60 -120.39 -45.22
			# 'stand': [0, 75, -120, -45],
			# 'sit': [0, 90, -90, -90],

			# engine
			'serialPort': '/dev/tty.usbserial-A506BOT5',
			# 'write': 'bulk'
		}
		self.leg = Leg4(data)
		self.engine = Engine(data, AX12)

	def angles(self):
		fa = [
			[150, 240, 70, 240],  # servo angles [0-300]
			[150, 220, 100, 150],
			[150, 200, 170, 60],
			[150, 180, 170, 240],
			[150, 200, 170, 150],
			[150, 240, 150, 150]
		]
		for a in fa:
			self.engine.moveLegsAnglesArray(a, 100)
			time.sleep(2)

	def gait(self):
		legs = {
			0: [
				[150, 240, 70, 240],  # servo angles [0-300]
				[150, 220, 100, 150],
				[150, 200, 170, 60],
				[150, 180, 170, 240],
				[150, 200, 170, 150],
				[150, 240, 150, 150]
			]  # servo angles [0-300]
		}
		self.engine.moveLegsGait(legs, speed=100)
		time.sleep(1)

	# def pts(self):
	# 	fp = [
	# 		[]
	# 	]
	# 	for p in fp:
	# 		a = self.engine
	# 		self.engine.moveLegsAngles(a, 100)
	# 		time.sleep(1)


def main():
	test = LegTest()

	try:
		# test.angles()
		test.gait()
		# test.pts()
	except KeyboardInterrupt:
		print('bye ...')
		time.sleep(1)


if __name__ == '__main__':
	main()
