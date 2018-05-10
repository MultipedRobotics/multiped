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
from quadruped import Leg4
from pyservos import AX12
import time
from math import pi


class RobotTest(object):
	def __init__(self):
		data = {
			# [ length, (limit_angles), offset_angle] - units:mm or degrees
			'coxa':   [52, [-90, 90], 150],
			'femur':  [90, [-90, 90], 123],   # fixme
			'tibia':  [89, [-90, 120], 194],  # fixme
			'tarsus': [90, [-90, 90], 167],

			# gait
			# Angles: 0.00 75.60 -120.39 -45.22
			# 'stand': [0, 75, -120, -45],
			# 'stand': [0, 37, -139, -45],
			'standUnits': 'deg',
			'stand': [0, 160-123, 130-194, 100-167],
			# 'sit': [0, 90, -90, -90],

			# engine
			# 'serialPort': '/dev/tty.usbserial-A506BOT5',
			'serialPort': 'com6',
			# 'write': 'bulk'
		}
		self.leg = Leg4(data)
		neutral = self.leg.getNeutralPos()
		self.gait = DiscreteRippleGait(35.0, neutral)
		self.engine = Engine(data, AX12, wait=0.1)

	def static(self):
		angles = {
			2: [
				# DH [0, 94, -139, -45]
				[150+0, 150+50, 220-139, 150-45]
			]
		}
		self.engine.moveLegsGait(angles, speed=50)  # send commands to servos
		# time.sleep(5)
		print(angles)
		print('len', len(angles[2]))

	def get_point(self, angles):
		"""
		debug
		angles: list of servo angles [s1,s2,s3,s4]
		returns: foot location (x,y,z)
		"""
		return self.leg.forward(*angles)

	def get_angle(self, pt):
		"""
		debug
		pt: tuple of foot location (x,y,z)
		return: list of servo angles [s1,s2,s3,s4], where s1 is the coxa and

		"""
		return self.leg.inverse(*pt)

	def pose_pt(self):
		pass

	def walk(self):
		# predefined walking path
		# x, y, rotation
		path = [
			[1.0, 0, 0],
			[1.0, 0, 0],
			# [1.0, 0, 0],
			# [1.0, 0, 0],
			# [1.0, 0, 0],
			# [1.0, 0, 0],
			# [1.0, 0, 0],
			# [1.0, 0, 0],
			# [1.0, 0, 0],
			# [1.0, 0, 0],
			[0, 0, pi/4],
			[0, 0, pi/4],
			[0, 0, pi/4],
			[0, 0, -pi/4],
			[0, 0, -pi/4],
			[0, 0, -pi/4],
			# [-1.0, 0, 0],
			# [-1.0, 0, 0],
			# [-1.0, 0, 0],
			# [-1.0, 0, 0],
			# [-1.0, 0, 0],
			# [-1.0, 0, 0],
			# [-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
		]

		for cmd in path:
			pts = self.gait.oneCycle_alt(*cmd)        # get 3d feet points
			angles = self.leg.generateServoAngles(pts)  # get servo angles

			# only move 1 leg, remove others from commands
			# angles.pop(0)
			# angles.pop(1)
			# angles.pop(3)

			self.engine.moveLegsGait(angles, speed=100)  # send commands to servos
			# time.sleep(5)
			print(cmd)
			# print(angles)
			# print('len', len(angles[2]))


def main():
	test = RobotTest()

	try:
		# test.walk()
		# test.static()
		# a = [0, 160-123, 130-194, 100-167]
		# print(test.get_point(a))  # (196.89869392004982, 0.0, -76.0225669165195)
		p = [160,0,-70]
		print(test.get_angle(p))
	except KeyboardInterrupt:
		print('bye ...')
		time.sleep(1)


if __name__ == '__main__':
	main()
