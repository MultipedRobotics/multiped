#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
# from quadruped import Engine
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
			'stand': [0, 75, -120, -45],
			'sit': [0, 90, -90, -90],

			# engine
			'serialPort': '/dev/tty.usbserial-A506BOT5',
			# 'write': 'bulk'
		}
		self.leg = Leg4(data)

	def array(self):
		fa = [
			[0,0,0,0]
		]
		for a in fa:
			self.leg.forward(*a)
			time.sleep(2)


def main():
	test = LegTest()

	try:
		test.array()
		# test.single()
	except KeyboardInterrupt:
		print('bye ...')
		time.sleep(1)


if __name__ == '__main__':
	main()
