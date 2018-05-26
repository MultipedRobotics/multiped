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
import platform


class RobotTest(object):
	def __init__(self):
		bcm_pin = None
		if platform.system() == 'Darwin':
			ser = '/dev/tty.usbserial-A506BOT5'
		elif platform.system() == 'Linux':
			ser = '/dev/serial0'
			bcm_pin = 4
		else:
			ser = 'com5'

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
			# 'standUnits': 'deg',
			'stand': [0, 160-123, 130-194, 100-167],
			'sit': [0, 250-123, 80-194, 60-167],

			# engine
			'serialPort': ser,
			# 'write': 'bulk'
		}
		self.leg = Leg4(data)
		neutral = self.leg.getNeutralPos()
		self.gait = DiscreteRippleGait(55.0, neutral)
		# self.gait.scale = 100
		self.engine = Engine(data, AX12, wait=0.3, bcm_pin=bcm_pin)

		self.stand()

	def __del__(self):
		self.sit()

	# def static(self):
	# 	angles = {
	# 		2: [
	# 			# DH [0, 94, -139, -45]
	# 			[150+0, 123+50, 194-139, 167-45]
	# 		]
	# 	}
	# 	self.engine.moveLegsGait(angles, speed=50)  # send commands to servos
	# 	# time.sleep(5)
	# 	print(angles)
	# 	print('len', len(angles[2]))

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

	def pose_pt(self, leg, pt):
		pts = {
			leg: [pt]
		}
		angles = self.leg.generateServoAngles(pts)
		print(angles)
		self.engine.moveLegsGait(angles, speed=100)
		pass

	def walk(self):
		# predefined walking path
		# x, y, rotation
		path = [
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			# [1.0, 0, 0],
			# [1.0, 0, 0],
			# [1.0, 0, 0],
			# [1.0, 0, 0],
			# [1.0, 0, 0],
			# [1.0, 0, 0],
			# [0, 0, pi/4],
			# [0, 0, pi/4],
			# [0, 0, pi/4],
			# [0, 0, -pi/4],
			# [0, 0, -pi/4],
			# [0, 0, -pi/4],
			# [-1.0, 0, 0],
			# [-1.0, 0, 0],
			# [-1.0, 0, 0],
			# [-1.0, 0, 0],
			# [-1.0, 0, 0],
			# [-1.0, 0, 0],
			# [-1.0, 0, 0],
			# [-1.0, 0, 0],
			# [-1.0, 0, 0],
			# [-1.0, 0, 0],
		]

		for cmd in path:
			pts = self.gait.oneCycle_alt(*cmd)        # get 3d feet points
			# pts = self.gait.command(cmd)        # get 3d feet points
			angles = self.leg.generateServoAngles(pts)  # get servo angles

			# only move 1 leg, remove others from commands
			# angles.pop(0)
			# angles.pop(1)
			# angles.pop(3)

			self.engine.moveLegsGait(angles, speed=50)  # send commands to servos
			time.sleep(5)
			print(cmd)
			# print(angles)
			# print('len', len(angles[2]))

	def step(self, leg, p1, p2, lift):
		"""
		Pick the foot up and set it down
		leg - which leg number 0-3
		p1 - start (x,y,z)
		p2 - stop (x,y,z)
		lift - how high to lift the foot
		"""


	def sit(self):
		angles = self.leg.sit()
		self.engine.moveLegsGait(angles, speed=200)
		time.sleep(2)

	def stand(self):
		angles = self.leg.stand()
		self.engine.moveLegsGait(angles, speed=200)
		time.sleep(2)


def main():
	test = RobotTest()
	time.sleep(2)

	try:
		# test.stand()
		time.sleep(3)
		test.walk()
		# test.sitstand()
		# test.pose_pt(2,[140,0,-10])
		# a = [0, 160-123, 130-194, 100-167]
		# print(test.get_point(a))  # (196.89869392004982, 0.0, -76.0225669165195)
		# p = [160,0,-70]
		# print(test.get_angle(p))
		# test.sit()
		# time.sleep(2)
	except KeyboardInterrupt:
		print('bye ...')
		time.sleep(1)


if __name__ == '__main__':
	main()
