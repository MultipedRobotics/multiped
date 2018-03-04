##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
from math import sin, cos, acos, atan2, sqrt, pi
from math import radians as d2r
# from math import degrees as r2d
# import logging
# from .Servo import Servo

# logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.ERROR)


class Servo(object):
	"""
	Servo hold the parameters of a servo, it doesn't talk to real servos. This
	class does the conversion between DH angles to real servo angles
	"""
	# _angle = 0.0  # current angle
	# offset = 150.0  # angle offset default, see above for explaination
	# minAngle = -150.0
	# maxAngle = 150.0

	def __init__(self, ID, minmax, offset=150):
		self.offset = offset
		self.minAngle = minmax[0]
		self.maxAngle = minmax[1]
		self.id = ID

	def DH2Servo(self, angle):
		"""
		Sets the servo angle and clamps it between [limitMinAngle, limitMaxAngle].
		"""
		# saturates the angle if it is outside of the limits
		if self.minAngle > angle or angle > self.maxAngle:
			# raise Exception('DH2Servo {} > {} > {}'.format(self.minAngle, angle, self.maxAngle))
			# print('DH2Servo[{}] error {:.0f} > {:.0f} > {:.0f}'.format(self.id, self.minAngle, angle, self.maxAngle))
			# pass

			if self.minAngle > angle:
				print('DH2Servo[{}] error {:.0f} > {:.0f}'.format(self.id, self.minAngle, angle))
				angle = self.minAngle
			elif self.maxAngle < angle:
				print('DH2Servo[{}] error {:.0f} > {:.0f}'.format(self.id, angle, self.maxAngle))
				angle = self.maxAngle

		return angle+self.offset


class LegException(Exception):
	pass


class Leg4(object):
	"""
	Leg class outputs the servo angles for some requested foot location (x,y,z)

	Leg knows:
	- leg dimensions
	- number of servos and their parameters/limits
	- fk/ik equations
	- sit/stand sequence
	"""
	# these are fixed by the 3D printing, not changing
	coxaLength = None
	tibiaLength = None
	femurLength = None
	tarsusLength = None
	sit_angles = None
	stand_angles = None

	def __init__(self, params):
		"""
		Each leg has 4 servos/channels
		"""
		# setup kinematics and servos
		self.servos = []
		for ID, seg in enumerate(['coxa', 'femur', 'tibia', 'tarsus']):
			# self.coxaLength = params[seg][0]
			self.servos.append(Servo(ID, params[seg][1], params[seg][2]))

		self.coxaLength = params['coxa'][0]
		self.femurLength = params['femur'][0]
		self.tibiaLength = params['tibia'][0]
		self.tarsusLength = params['tarsus'][0]

		self.sit_angles = params['sit']
		self.stand_angles = params['stand']

		pp = self.forward(*self.stand_angles)
		aa = self.inverse(*pp)
		print('stand', pp)
		print('stand', aa)
		# exit()

	def __del__(self):
		pass

	def sit(self):
		# TODO: animate this or slow down the motion so we don't break anything
		# self.moveFootAngles(*self.sit_angles)
		pass

	def stand(self):
		# TODO: animate this or slow down the motion so we don't break anything
		# self.moveFootAngles(*self.stand_angles)
		pass

	def forward(self, t1, t2, t3, t4, degrees=True):
		"""
		Forward kinematics of the leg, note, default angles are all degrees.
		The input angles are referenced to the DH frame arrangement.
		"""
		l1 = self.coxaLength
		l2 = self.femurLength
		l3 = self.tibiaLength
		l4 = self.tarsusLength

		if degrees:
			t1 = d2r(t1)
			t2 = d2r(t2)
			t3 = d2r(t3)
			t4 = d2r(t4)

		x = (l1 + l2*cos(t2) + l3*cos(t2 + t3) + l4*cos(t2 + t3 + t4))*cos(t1)
		y = (l1 + l2*cos(t2) + l3*cos(t2 + t3) + l4*cos(t2 + t3 + t4))*sin(t1)
		z = l2*sin(t2) + l3*sin(t2 + t3) + l4*sin(t2 + t3 + t4)

		return (x, y, z,)

	def inverse(self, x, y, z, o=90, degrees=True):
		"""
		Azimuth angle is between x and w and lies in the x-y plane

				   ^ x
			 w     |
			   \   |
			 l1 \  |
				 \ |
				  \|
		<----------+ (z is out of the page - right hand rule)
		y

		Most of the robot arm move in the plane defined by w-z

		^ z      l3
		|      o-----o
		|     /       \ l4
		|    / l2      E
		|   /
		+--o-------------> w
		 l1

		l1: coxa
		l2: femur
		l3: tibia
		l4: tarsus

		All joint angles returned are in degrees: (t1, t2, t3, t4)
		"""
		def cosinelaw(a, b, c):
			# cosine law only used by this function
			# cos(g) = (a^2+b^2-c^2)/2ab
			return acos((a**2+b**2-c**2)/(2*a*b))

		l1 = self.coxaLength
		l2 = self.femurLength
		l3 = self.tibiaLength
		l4 = self.tarsusLength

		t1 = atan2(y, x)

		if degrees:
			o = o*pi/180

		try:
			w = sqrt(x**2 + y**2) - l1
			j4w = w + l4*cos(o)
			j4z = z + l4*sin(o)
			r = sqrt(j4w**2 + j4z**2)
			g1 = atan2(j4z, j4w)
			g2 = cosinelaw(l2, r, l3)
			t2 = g1+g2

			t3 = pi+cosinelaw(l2, l3, r)

			j2w = l2*cos(t2)
			j2z = l2*sin(t2)
			c = sqrt((w-j2w)**2 + (z-j2z)**2)
			t4 = pi+cosinelaw(l3, l4, c)
		except Exception as e:
			print('inverse({:.2f},{:.2f},{:.2f},{:.2f})'.format(x, y, z, o))
			print('Error:', e)
			raise

		def check(t):
			if t > 150*pi/180:
				t -= 2*pi
			return t

		t1 = check(t1)
		t2 = check(t2)
		t3 = check(t3)
		t4 = check(t4)

		if degrees:
			t1 *= 180/pi
			t2 *= 180/pi
			t3 *= 180/pi
			t4 *= 180/pi

		return (t1, t2, t3, t4)

	def generateServoAngles(self, footLoc):
		"""
		This is a bulk process and takes all of the foot locations for an entire
		sequence of a gait cycle. It handles all legs at once.

		footLoc: locations of feet from gait
		[
			[pos0, pos1, pos2, pos3], # step0
			...
		]

		[   step0      step1   ...
			[(x,y,z), (x,y,z), ...] # leg0
			[(x,y,z), (x,y,z), ...] # leg1
			...
		]

		return
		[   step 0          step 1         ...
			[[t1,t2,t3,t4], [t1,t2,t3,t4], ...] # leg0
			[[t1,t2,t3,t4], [t1,t2,t3,t4], ...] # leg1
			...
		]
		"""
		# TODO: fix this to handle N legs, right now it only does 4

		angles = [[], [], [], []]

		for f in footLoc:
			a, b, c, d = f
			# calculate the inverse DH angles
			a = self.inverse(*a)  # s0,s1,s2,s3
			b = self.inverse(*b)  # s4,s5,s6,s7
			c = self.inverse(*c)  # ...
			d = self.inverse(*d)

			self.pprint([a, b, c, d])

			for i, s in enumerate([a, b, c, d]):
				tmp = [0]*4
				tmp[0] = self.servos[0].DH2Servo(s[0])
				tmp[1] = self.servos[1].DH2Servo(s[1])
				tmp[2] = self.servos[2].DH2Servo(s[2])
				tmp[3] = self.servos[3].DH2Servo(s[3])
				angles[i].append(tmp)

		return angles

	def pprint(self, step):
		print('*'*25)
		for leg in step:
			print('  DH: [{:.0f} {:.0f} {:.0f} {:.0f}]'.format(*leg))

	def moveFoot(self, x, y, z):
		"""
		generates servo angles to move the foot to coordinates [x,y,z]. This
		is individual and not intended for walking, but something else.
		"""
		pass

	def getNeutralPos(self):
		return self.forward(*self.stand_angles)
