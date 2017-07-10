#!/usr/bin/env python

##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
import numpy as np
from math import cos, sin, sqrt, pi
# from math import radians as d2r
# from Servo import Servo
# import time


def rot_z_tuple(t, c):
	"""
	t - theta [radians]
	c - [x,y,z]
	return - (x,y,z) tuple rotated about z-axis
	"""
	ans = (
		c[0]*cos(t)-c[1]*sin(t),
		c[0]*sin(t)+c[1]*cos(t),
		c[2]
	)

	return ans


# make a static method in Gait? Nothing else uses it
def rot_z(t, c):
	"""
	t - theta [radians]
	c - [x,y,z]
	return - [x,y,z] numpy array rotated about z-axis
	"""
	ans = np.array([
		c[0]*cos(t)-c[1]*sin(t),
		c[0]*sin(t)+c[1]*cos(t),
		c[2]
	])
	# ans = np.array(rot_z_tuple(t, c))

	return ans


class Gait(object):
	"""
	Base class for gaits. Gait only plan all foot locations for 1 complete cycle
	of the gait.
	"""
	# these are the offsets of each leg
	legOffset = [0, 6, 3, 9]
	# frame rotations for each leg
	cmrot = [pi/4, -pi/4, -3*pi/4, 3*pi/4]
	frame = [-pi/4, pi/4, 3*pi/4, -3*pi/4]  # this seem to work better ... wtf?
	moveFoot = None
	rest = None
	scale = 50.0

	def __init__(self, rest):
		# the resting or idle position/orientation of a leg
		self.rest = rest
		# self.moveFoot = mf
		# self.write = w

	def command(self, cmd):
		"""
		func is the quadruped move foot function for a specific leg
		"""
		x, y, rz = cmd
		d = sqrt(x**2+y**2)

		# commands should be unit length, oneCyle scales it
		if 1.0 < d:
			x /= d
			y /= d

		# handle no movement command ... do else where?
		if d < 0.1 and abs(rz) < 0.1:
			x = y = 0.0
			rz = 0.0

			return None

		# if abs(rz) < 0.001:
		# 	rz = 0.0

		return self.oneCycle(x, y, rz)

	def oneCycle(x, y, rz):
		print('*** wrong function! ***')
		return None


class DiscreteRippleGait(Gait):
	"""
	Discrete 12 step gait
	"""
	steps = 0

	def __init__(self, h, r):
		Gait.__init__(self, r)
		self.phi = [9/9, 6/9, 3/9, 0/9, 1/9, 2/9, 3/9, 4/9, 5/9, 6/9, 7/9, 8/9]  # foot pos in gait sequence
		maxl = h  # lifting higher gives me errors
		minl = maxl/2
		self.z = [minl, maxl, minl, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # leg height
		self.steps = len(self.phi)

	def eachLeg(self, index, cmd):
		"""
		interpolates the foot position of each leg
		cmd:
			linear (mm)
			angle (rads)
		"""
		rest = self.rest
		i = index
		phi = self.phi[i]
		xx, yy, rzz = cmd

		# rotational commands -----------------------------------------------
		angle = rzz/2-rzz*phi
		rest_rot = rot_z(-angle, rest)

		# create new move command
		move = np.array([
			xx/2 - phi*xx,
			yy/2 - phi*yy,
			self.z[i]
		])

		# new foot position: newpos = rot + move ----------------------------
		newpos = move + rest_rot
		# print('New  [](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(newpos[0], newpos[1], newpos[2]))
		return newpos

	def oneCycle(self, x, y, rz):
		scale = self.scale
		cmd = (scale*x, scale*y, rz)
		ret = []  # 4 leg foot positions for the entire 12 count cycle is returned

		for i in range(0, self.steps):  # iteration, there are 12 steps in gait cycle
			footPos = []
			for legNum in [0, 2, 1, 3]:  # order them diagonally
				# rcmd = self.calcRotatedOffset(cmd, legNum)
				rcmd = rot_z_tuple(self.frame[legNum], cmd)
				index = (i + self.legOffset[legNum]) % 12
				pos = self.eachLeg(index, rcmd)  # move each leg appropriately
				# print('Foot[{}]: {:.2f} {:.2f} {:.2f}'.format(legNum, *(pos)))
				# if legNum == 0: print('New  [{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(i, pos[0], pos[1], pos[2]))
				footPos.append([index, legNum, pos])  # all in leg frame
			# print('footPos', footPos)

			# corr = Correction()
			# c = corr.calcCorrection(footPos)
			# feet = corr.rotateFeetCorrected(footPos, c)

			ret.append(footPos)  # 4 feet at index i: [index, legNum, footposition]

# <<<<<<< HEAD:quadruped/Gait.py
		return ret
# =======
# 			feet = footPos
# 			# print('----------------------------')
# 			for foot in feet:
# 				legNum = foot[1]
# 				ft = foot[2]
# 				self.moveFoot(legNum, ft)
# 				# print('Foot[{}]: {:.2f} {:.2f} {:.2f}'.format(legNum, *ft))
#
# 			# Servo.bulkWrite(Servo.ser)
# 			# Servo.syncWrite(Servo.ser)
# 			self.write()
# 			time.sleep(0.1)
# >>>>>>> master:quadruped/quadruped/Gait.py


# class ContinousRippleGait(Gait):
# 	alpha = 1.0
#
# 	def __init__(self, h, r):
# 		Gait.__init__(self)
# 		self.height = h
# 		self.rest = r
#
# 	@staticmethod
# 	def phi(x):
# 		"""
# 		The phase
# 		"""
# 		phi = 0.0
# 		if x <= 3.0:
# 			phi = 1/3*(3.0-x)
# 		else:
# 			phi = 1/9*(x-3)
# 		return phi
#
# 	def z(self, x):
# 		"""
# 		Leg height
#
# 		duty cycle:
# 			0-3: leg lifted
# 			3-12: leg on ground
# 			duty = (12-3)/12 = 0.75 = 75% a walking gait
# 		"""
# 		height = self.height
# 		z = 0.0
# 		if x <= 1:
# 			z = height/1.0*x
# 		elif x <= 2.0:
# 			z = height
# 		elif x <= 3.0:
# 			z = -height/1.0*(x-2.0)+height
# 		return z
#
# 	def eachLeg(self, index, cmd):
# 		"""
# 		interpolates the foot position of each leg
# 		"""
# 		rest = self.rest
# 		i = (index*self.alpha) % 12
# 		phi = self.phi(i)
# 		z = self.z(i)
#
# 		# rotational commands -----------------------------------------------
# 		angle = cmd['angle']/2-cmd['angle']*phi
# 		rest_rot = rot_z(-angle, rest)
# 		# rest_rot[2] = 0  # let linear handle z height
#
# 		# linear commands ----------------------------------------------------
# 		linear = cmd['linear']
# 		xx = linear[0]
# 		yy = linear[1]
#
# 		# create new move command
# 		move = np.array([
# 			xx/2 - phi*xx,
# 			yy/2 - phi*yy,
# 			z
# 		])
#
# 		# new foot position: newpos = rot + move ----------------------------
# 		newpos = move + rest_rot
# 		return newpos
