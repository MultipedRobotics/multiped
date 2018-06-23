##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
from math import cos, sin, sqrt, pi


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
	ans = [
		c[0]*cos(t)-c[1]*sin(t),
		c[0]*sin(t)+c[1]*cos(t),
		c[2]
	]

	return ans


class Gait(object):
	"""
	Base class for gaits. Gait only plan all foot locations for 1 complete cycle
	of the gait.

	Like to add center of mass (CM) compensation, so we know the CM is always
	inside the stability triangle.

	Gait knows:
	- how many legs
	- leg stride (neutral position)
	"""
	# these are the offsets of each leg
	legOffset = [0, 6, 3, 9]
	# frame rotations for each leg
	# cmrot = [pi/4, -pi/4, -3*pi/4, 3*pi/4]
	# frame = [-pi/4, pi/4, 3*pi/4, -3*pi/4]  # this seem to work better ... wtf?
	frame = [pi/4, -pi/4, -3*pi/4, 3*pi/4]
	moveFoot = None
	rest = None
	scale = 50.0

	def __init__(self, rest):
		# the resting or idle position/orientation of a leg
		self.rest = rest

	def command(self, cmd):
		"""
		Send a command to the quadruped
		cmd: [x, y, rotation about z-axis], the x,y is a unit vector and
		rotation is in radians
		"""
		x, y, rz = cmd
		d = sqrt(x**2+y**2)

		# handle no movement command ... do else where?
		if d <= 0.1 and abs(rz) < 0.1:
			x = y = 0.0
			rz = 0.0
			return None
		# commands should be unit length, oneCyle scales it
		elif 0.1 < d:
			x /= d
			y /= d
		else:
			return None

		angle_limit = pi/2
		if rz > angle_limit:
			rz = angle_limit
		elif rz < -angle_limit:
			rz = -angle_limit

		return self.oneCycle_alt(x, y, rz)

	def oneCycle_alt(slef, x, y, rz):
		raise Exception('*** Gait: wrong function, this is base class! ***')


class DiscreteRippleGait(Gait):
	"""
	Discrete 12 step gait
	"""
	steps = 0

	def __init__(self, height, rest):
		"""
		height: added to z
		rest: the neutral foot position
		"""
		Gait.__init__(self, rest)
		self.phi = [8/8, 7/8, 1/8, 0/8, 1/8, 2/8, 3/8, 4/8, 5/8, 6/8, 7/8, 8/8]
		self.setLegLift(height)
		self.steps = len(self.phi)

	def setLegLift(self, lift):
		#           0     1     2    3    4    5    6    7    8    9   10   11
		self.z = [0.0, lift, lift, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # leg height

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
		move = [
			xx/2 - phi*xx,
			yy/2 - phi*yy,
			self.z[i]
		]

		# new foot position: newpos = rot + move ----------------------------
		# newpos = move + rest_rot
		newpos = [0, 0, 0]
		newpos[0] = move[0] + rest_rot[0]
		newpos[1] = move[1] + rest_rot[1]
		newpos[2] = move[2] + rest_rot[2]

		# print('New  [](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(newpos[0], newpos[1], newpos[2]))
		return newpos

	def oneCycle(self, x, y, rz):
		"""
		direction of travel x, y (2D plane) or rotation about z-axis
		Returns 1 complete cycle for all 4 feet (x,y,z)
		"""

		# check if x, y, rz is same as last time commanded, if so, return
		# the last cycle response, else, calculate a new response
		# ???

		scale = self.scale
		cmd = (scale*x, scale*y, rz)
		ret = {
			0: [],
			1: [],
			2: [],
			3: []
		}  # 4 leg foot positions for the entire 12 count cycle is returned

		# iteration, there are 12 steps in gait cycle, add a 13th so all feet
		# are on the ground at the end, otherwise one foot is still in the air
		for i in range(0, self.steps)+[0]:
			for legNum in [0, 1, 2, 3]:  # order them diagonally
				rcmd = rot_z_tuple(self.frame[legNum], cmd)
				index = (i + self.legOffset[legNum]) % self.steps
				pos = self.eachLeg(index, rcmd)  # move each leg appropriately
				# print('Foot[{}]: {:.2f} {:.2f} {:.2f}'.format(legNum, *(pos)))
				ret[legNum].append(pos)

		for legNum in [0, 1, 2, 3]:
			print('Leg[{}]---------'.format(legNum))
			for i, pt in enumerate(ret[legNum]):
				print('  {:2}: {:7.2f} {:7.2f} {:7.2f}'.format(i, *pt))

		return ret

	# def oneCycle_alt2(self, x, y, rz):
	# 	"""
	# 	direction of travel x, y (2D plane) or rotation about z-axis
	# 	Returns 1 complete cycle for all 4 feet (x,y,z)
	# 	"""
	#
	# 	# check if x, y, rz is same as last time commanded, if so, return
	# 	# the last cycle response, else, calculate a new response
	# 	# ???
	#
	# 	scale = self.scale
	# 	cmd = (scale*x, scale*y, rz)
	# 	ret = {
	# 		0: [],
	# 		1: [],
	# 		2: [],
	# 		3: []
	# 	}  # 4 leg foot positions for the entire 12 count cycle is returned
	#
	# 	speed = 100
	#
	# 	# iteration, there are 12 steps in gait cycle, add a 13th so all feet
	# 	# are on the ground at the end, otherwise one foot is still in the air
	# 	for i in range(0, self.steps)+[0]:
	# 		for legNum in [0, 1, 2, 3]:  # order them diagonally
	# 			rcmd = rot_z_tuple(self.frame[legNum], cmd)
	# 			index = (i + self.legOffset[legNum]) % self.steps
	# 			pos = self.eachLeg(index, rcmd)  # move each leg appropriately
	# 			# print('Foot[{}]: {:.2f} {:.2f} {:.2f}'.format(legNum, *(pos)))
	# 			ret[legNum].append((pos, speed,))
	#
	# 	for legNum in [0, 1, 2, 3]:
	# 		print('Leg[{}]---------'.format(legNum))
	# 		for i, pt in enumerate(ret[legNum]):
	# 			print('  {}:'.format(i), pt)
	#
	# 	return ret
