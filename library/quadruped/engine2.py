
from __future__ import print_function
from __future__ import division
import time



# class Servo(object):
# 	_angle = 0.0  # current angle
# 	_offset = 150.0  # angle offset default, see above for explaination
# 	minAngle = -150.0
# 	maxAngle = 150.0
# 	ID = 0
#
# 	def __init__(self, ID, min, max, offset):
# 		pass
#
# 	@property
# 	def angle(self):
# 		"""
# 		Returns the current servo angle
# 		"""
# 		return self._angle
#
# 	@angle.setter
# 	def angle(self, angle):
# 		"""
# 		Sets the servo angle and clamps it between [limitMinAngle, limitMaxAngle].
# 		"""
#
# 		# saturates the angle if it is outside of the limits
# 		if self.minAngle > angle or angle > self.maxAngle:
# 			# raise Exception('@angle.setter {} > {} > {}'.format(self.minAngle, angle, self.maxAngle))
# 			print('@angle.setter error {} > {} > {}'.format(self.minAngle, angle, self.maxAngle))
#
# 			if self.minAngle > angle:
# 				angle = self.minAngle
# 			elif self.maxAngle < angle:
# 				angle = self.maxAngle


class Engine(object):
	sync = []

	def __init__(self, data, servoType):
		"""
		data: serial port to use, if none, then use dummy port
		kind: AX12 or XL320
		"""

		# # check for missing data
		# if 'servos per leg' not in data:
		# 	raise Exception('Engine() needs to know number of servos per leg')

		# determine serial port
		# default to fake serial port
		if 'serialPort' in data:
			try:
				self.serial = ServoSerial(data['serialPort'])
				print('Using servo serial port: {}'.format(data['serialPort']))

			except Exception as e:
				print(e)
				print('bye ...')
				exit(1)
		else:
			print('*** Using dummy serial port!!! ***')
			self.serial = ServoSerial('dummy')
			# raise Exception('No serial port given')

		self.packet = Packet(kind)
		# pkt = ax.makeServoPacket(1, 158.6)  # move servo 1 to 158.6 degrees

		# angle offsets to line up with fk
		# self.legs = []

		# spl = data['servos per leg']
		# for i in range(0, 4):  # 4 legs
		# 	channel = i*spl  # x servos per leg
		# 	if spl == 3:
		# 		self.legs.append(
		# 			Leg3([channel+1, channel+2, channel+3])
		# 		)
		# 	elif spl == 4:
		# 		self.legs.append(
		# 			Leg4([channel+1, channel+2, channel+3, channel+4])
		# 		)
		# 	else:
		# 		raise Exception('Engine() invalid number of servos per leg:', spl)

	# def push(self, ID, angle, speed=None):
	# 	self.sync.append((ID, angle))

	def moveLegsPosition(self, legs):
		"""
		this only does position
		[   step 0          step 1         ...
			[[t1,t2,t3,t4], [t1,t2,t3,t4], ...] # leg0
			[[t1,t2,t3,t4], [t1,t2,t3,t4], ...] # leg1
			...
		]
		"""
		# build bulk message
		# FIXME: hard coded for 4 legs
		for step in zip(*legs):  # servo angles for each leg at each step
			data = [] # [id, lo, hi, id, lo, hi, ...]
			# leg 0: 0 1 2 3
			for i, leg in enumerate(step):  # step = [leg0, leg1, leg2, leg3]
				for j, servo in enumerate(leg):  # leg = [servo0, servo1, servo2, servo3]
					data.append(4*i+j)      # servo ID
					a, b = angle2int(a[0])  # angle
					data.append(a)
					data.append(b)

			# FIXME: hard coded to AX
			pkt = self.packet.makeSyncWritePacket(AX12.GOAL_POSITION, data)
			self.serial.sendPkt(pkt)
			time.sleep(.3)

	# def write(self):
	# 	# use self.sync to build packet
	#
	# 	ret = serial.sendPkt(pkt)
	# 	# ret = serial.sendPkt(pkt)
