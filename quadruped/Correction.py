
from __future__ import print_function
from __future__ import division
import numpy as np
from numpy.linalg import norm
# import logging
from math import cos
# from math import sin
# from math import sqrt
from math import pi
from Gait import rot_z


class RobotTransform(object):
	"""
	Converts pts between the leg and body frame.
	"""
	def __init__(self, radius):
		"""
		in:
			radius - radius of body from CM in mm
			anglesB2L - angles to transform between body and leg frames
		"""
		# cmrot
		self.leg2body = [pi/4, -pi/4, -3*pi/4, 3*pi/4]  # legs to body frame # orig
#         self.leg2body = [-pi/4, pi/4, 3*pi/4, -3*pi/4]  # legs to body frame
		# frame
		self.body2leg = [-pi/4, pi/4, 3*pi/4, -3*pi/4]  # body to leg frame # orig
#         self.body2leg = [pi/4, -pi/4, -3*pi/4, 3*pi/4]  # body to leg frame
		# account for base, in base frame
		cm = radius*cos(pi/4)
		self.base = [
			np.array([cm, cm, 0]),
			np.array([cm, -cm, 0]),
			np.array([-cm, -cm, 0]),
			np.array([-cm, cm, 0])
		]

	def leg2Body(self, legNum, pts):
		"""
		Converts points from leg_frame to body_frame
		"""
		pts2 = rot_z(self.leg2body[legNum], pts) + self.base[legNum]
		return pts2

	def body2Leg(self, legNum, pts):
		"""
		Converts points from body_frame to leg_frame
		"""
		pts2 = rot_z(self.body2leg[legNum], pts-self.base[legNum])
		return pts2


class Correction(object):
	def __init__(self):
		pass

	@staticmethod
	def inside(feet, prnt=False):
		"""
		Determine if a point P is inside of a triangle composed of points
		A, B, and C.
		pts = [A,B,C]
		P = [0,0] at the center of mass of the robot
		returns True (inside triangle) or False (outside the triangle)
		"""
		pts = []
		for p in feet:
			if isinstance(p, np.ndarray):
				pts.append(p)

		# print('inSideCM pts:', pts)
		A = pts[0][0:2]
		B = pts[1][0:2]
		C = pts[2][0:2]
		P = np.array([0, 0])  # CM is at the center :)

		# Compute vectors
		v0 = C - A
		v1 = B - A
		v2 = P - A

		# Compute dot products
		dot00 = np.dot(v0, v0)
		dot01 = np.dot(v0, v1)
		dot02 = np.dot(v0, v2)
		dot11 = np.dot(v1, v1)
		dot12 = np.dot(v1, v2)

		# Compute barycentric coordinates
		invDenom = 1 / (dot00 * dot11 - dot01 * dot01)
		u = (dot11 * dot02 - dot01 * dot12) * invDenom
		v = (dot00 * dot12 - dot01 * dot02) * invDenom

		if prnt:
			print(u, v)

		# Check if point is in triangle
		ans = ((u >= 0) and (v >= 0) and (u + v < 1))

		print('inside():', ans)
		return ans

	@staticmethod
	def lineIntersection(p1, p2, p3):
		"""
		Find the intersection of 2 lines.
		line 1: p1, p2
		line 2: p3, [0,0]
		"""
		x1 = p1[0]
		x2 = p2[0]
		x3 = p3[0]
		x4 = 0.0
		y1 = p1[1]
		y2 = p2[1]
		y3 = p3[1]
		y4 = 0.0

		denom = ((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4))
		if abs(denom) < 0.00001:
			# print('crap {}'.format(denom))
			return np.array([0, 0])
		x = ((x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4))/denom
		y = ((x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4))/denom
		return np.array([x, y])

	@staticmethod
	def vmin(a):
		"""
		Find the minimum vector in an array of 2D vectors.
		in = [[1,2], [2,3], ...]
		out = [1,2]
		"""
		minv = 0
		min_val = 1000000000000000
		for p in a:
			val = norm(p)
			if val < min_val:
				min_val = val
				minv = p
		return minv

	def correction(self, feet, movingFoot):
		"""
		Given the robot's foot locations, provide correction if the
		center of mass (CM) is outside the triangle formed by the 3
		foot locations.
		pts = [foot0, foot1, foot2, foot3]
		correction = [x,y,0]
		"""
#         a = []
#         for i in range(0, 3):
#             p0 = pts[i]
#             p1 = pts[(i+1) % 3]
#             xx = self.lineIntersection(p0, p1, cm0, cm1)
#             a.append(xx)
#         a = self.vmin(a)
#         correction = np.array([-a[0], -a[1], 0.0])
		# 0 1 2 3
		op = feet[(movingFoot + 2) % 4]
		p0 = feet[(movingFoot + 1) % 4]
		p1 = feet[(movingFoot + 3) % 4]
		a = self.lineIntersection(p0, p1, op)
		correction = np.array([-a[0], -a[1], 0.0])
		return correction

	def calcCorrection(self, feet):
		"""
		This take the feet positions, calculated by a Gait, and adjusts them
		to ensure the CM is inside of the stability triangle.

		in:
			feet = [[index, legNum, foot], ...] there are 4 of these
					index - tells if foot is up/down
					legNum - which leg [0-3]
					foot - (x,y,z) is converted to 2D
		out:
			correction = [x,y,0] is only a 2D correction
		"""
		temp = [0, 0, 0, 0]
		tf = RobotTransform(45)

		print('-------------------')
		print('calcCorrection()')
		movingFoot = 0
		for f in feet:
			index = f[0]
			foot = f[2]
			legNum = f[1]
			if index > 2:
				print('in foot: {:.2f} {:.2f}'.format(*foot[0:2]))
				ft = tf.leg2Body(legNum, foot)
				temp[legNum] = ft
				print('rotated foot: {:.2f} {:.2f}'.format(*ft[0:2]))
			else:
				movingFoot = legNum

		if not self.inside(temp):
			correction = 1.5*self.correction(temp, movingFoot)
		else:
			correction = np.array([0, 0, 0])
		return correction

	def rotateFeetCorrected(self, feet, correction):
		"""
		return: [[index, legNum, (x,y,z)], ...] corrected stationary feet positions
		"""
		tf = RobotTransform(45)
		ans = []
		for p in feet:  # p = [index, legNum, (x,y,z)]
			index = p[0]
			legNum = p[1]
			foot = p[2]
			if index > 2:  # check index to see if leg moving
				foot = tf.leg2Body(legNum, foot) + correction
				foot = tf.body2Leg(legNum, foot)
			ans.append([index, legNum, foot])
		return ans
