##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################


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
		self.minAngle = minmax[0]  # DH space
		self.maxAngle = minmax[1]  # DH space
		self.id = ID

	def DH2Servo(self, angle):
		"""
		Sets the servo angle and clamps it between [limitMinAngle, limitMaxAngle].
		"""
		# saturates the angle if it is outside of the limits
		# if self.minAngle > angle or angle > self.maxAngle:
		# 	# raise Exception('DH2Servo {} > {} > {}'.format(self.minAngle, angle, self.maxAngle))
		# 	# print('DH2Servo[{}] error {:.0f} > {:.0f} > {:.0f}'.format(self.id, self.minAngle, angle, self.maxAngle))
		# 	# pass
		#
		# 	if self.minAngle > angle:
		# 		print('DH2Servo[{}] error {:.0f} > {:.0f}'.format(self.id, self.minAngle, angle))
		# 		# angle = self.minAngle
		# 	elif self.maxAngle < angle:
		# 		print('DH2Servo[{}] error {:.0f} > {:.0f}'.format(self.id, angle, self.maxAngle))
		# 		# angle = self.maxAngle
		sangle = angle+self.offset
		if sangle > 300 or sangle < 0:
			raise Exception('{} angle out of range DH[-150,150]: {:.1f}   Servo[0,300]: {:.1f} deg'.format(self.id, angle, sangle))
		return sangle
