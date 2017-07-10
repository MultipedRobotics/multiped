#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
import numpy as np
from math import sin, cos, acos, atan2, sqrt, pi, fabs
from math import radians as d2r
from math import degrees as r2d
# import logging
from .Servo import Servo

# logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.ERROR)


class LegException(Exception):
	pass


class Leg(object):
	"""
	"""
	# these are fixed by the 3D printing, not changing
	coxaLength = 45.0
	tibiaLength = 55.0
	femurLength = 104.0
	s_limits = [
		[-90, 90],  # set limits
		[-90, 90],
		[-150, 0]
	]
	s_offsets = [150, 150, 150+90]  # angle offsets to line up with fk

	sit_raw = (150, 270, 100)
	stand_raw = (150, 175, 172)
	sit_angles = None
	stand_angles = None

	def __init__(self, channels):
		"""
		Each leg has 3 servos/channels
		"""
		if not len(channels) == 3:
			raise LegException('len(channels) != 3')

		Servo.bulkServoWrite = True

		# angle offsets to line up with fk
		self.servos = []
		for i in range(0, 3):
			self.servos.append(Servo(channels[i]))
			self.servos[i].setServoLimits(self.s_offsets[i], *self.s_limits[i])

		self.sit_angles = self.convertRawAngles(*self.sit_raw)
		# initAngles = [0, 0, -90+30]  # nico legs have a small offset
		# initAngles = [0, 45, -90+30-45]  # nico legs have a small offset
		initAngles = self.convertRawAngles(*self.stand_raw)
		self.stand_angles = initAngles
		self.foot0 = self.fk(*initAngles)  # rest/idle position of the foot/leg
		# print('foot0', self.foot0)

	def __del__(self):
		pass

	def sit(self):
		self.moveFootAngles(*self.sit_angles)

	def stand(self):
		self.moveFootAngles(*self.stand_angles)

	def convertRawAngles(self, a, b, c):
		return (a-self.s_offsets[0], b-self.s_offsets[1], c-self.s_offsets[2])

	def fk(self, a, b, g):
		"""
		Forward kinematics of the leg, note, angle are all degrees
		"""
		Lc = self.coxaLength
		Lf = self.femurLength
		Lt = self.tibiaLength

		a = d2r(a)
		b = d2r(b)
		g = d2r(g)

		foot = [
			(Lc + Lf*cos(b) + Lt*cos(b + g))*cos(a),
			(Lc + Lf*cos(b) + Lt*cos(b + g))*sin(a),
			Lf*sin(b) + Lt*sin(b + g)
		]

		return np.array(foot)

	def ik(self, x, y, z):
		"""
		Calculates the inverse kinematics from a given foot coordinate (x,y,z)[mm]
		and returns the joint angles[degrees]

		Reference (there are typos)
		https://tote.readthedocs.io/en/latest/ik.html

		If the foot (x,y,z) is in a position that does not produce a result (some
		numeric error or invalid foot location), the this returns None.
		"""
		# try:
		Lc = self.coxaLength
		Lf = self.femurLength
		Lt = self.tibiaLength

		if sqrt(x**2 + y**2) < Lc:
			print('too short')
			return None
		# elif z > 0.0:
		# 	return None

		a = atan2(y, x)
		f = sqrt(x**2 + y**2) - Lc
		# b1 = atan2(z, f)  # takes into account quadrent, z is neg

		# you have different conditions depending if z is pos or neg
		if z < 0.0:
			b1 = atan2(f, fabs(z))
		else:
			b1 = atan2(z, f)

		d = sqrt(f**2 + z**2)  # <---

		# print('ik pos: {} {} {}'.format(x,y,z))
		# print('d: {:.3f}  f: {:.3f}'.format(d,f))
		# print('Lc Lf Lt: {} {} {}'.format(Lc,Lf,Lt))
		# print('num: {:.3f}'.format(Lf**2 + d**2 - Lt**2))
		# print('den: {:.3f}'.format(2.0 * Lf * d))
		# print('acos: {:.2f}'.format((Lf**2 + d**2 - Lt**2) / (2.0 * Lf * d)))

		guts = ((Lf**2 + d**2 - Lt**2) / (2.0 * Lf * d))
		if 1.0 < guts or guts < -1.0:
			print('acos crap!: {:.3f} {:.3f} {:.3f} guts: {:.3f}'.format(x, y, z, guts))
			return None
		b2 = acos((Lf**2 + d**2 - Lt**2) / (2.0 * Lf * d))  # issues?
		b = b1 + b2
		g = acos((Lf**2 + Lt**2 - d**2) / (2.0 * Lf * Lt))

		# FIXES ###################################
		g -= pi  # fix to align fk and ik frames

		if z < 0.0:
			b -= pi/2  #
		##############################################
		# print('b1 b2: {:.2f} {:.2f}'.format(r2d(b1), r2d(b2)))
		# print('ik angles: {:.2f} {:.2f} {:.2f}'.format(r2d(a), r2d(b), r2d(g)))
		return r2d(a), r2d(b), r2d(g)  # coxaAngle, femurAngle, tibiaAngle

		# except Exception as e:
		# 	print('ik error:', e)
		# 	raise e

	def moveFoot(self, x, y, z):
		"""
		Attempts to move it's foot to coordinates [x,y,z]
		"""
		try:
			# a, b, c = self.ik(x, y, z)  # inverse kinematics
			# angles = [a, b, c]
			angles = self.ik(x, y, z)  # inverse kinematics
			# return angles
			if angles is None:
				print('something bad')
				return
			# print('angles: {:.2f} {:.2f} {:.2f}'.format(*angles))
			for i, servo in enumerate(self.servos):
				# print('i, servo:', i, servo)
				angle = angles[i]
				# print('servo {} angle {}'.format(i, angle))
				servo.angle = angle
			return angles

		except Exception as e:
			print (e)
			raise

	def moveFootAngles(self, a, b, c):
		"""
		Attempts to move it's foot to coordinates [x,y,z]
		"""
		try:
			for servo, angle in zip(self.servos, (a, b, c)):
				servo.angle = angle

		except:
			print('Leg::moveFootAngles() error')
			raise

	# def reset(self):
	# 	# self.angles = self.resting_position
	# 	self.move(*self.foot0)


if __name__ == "__main__":
	print('Hello cowboy!')
