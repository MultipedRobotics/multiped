# from .Gait import Gait
# from .Gait import rot_z
# import numpy as np
#
#
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
