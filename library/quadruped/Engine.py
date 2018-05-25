##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
from pyservos import ServoSerial
from pyservos import Packet
# from pyservos import AX12
from pyservos.packet import angle2int
from pyservos.utils import le
import time


class Engine(object):
	"""
	This class holds the serial port and talks to the hardware. Other classes (
	e.g., gait, legs and servos) do the calculations for walking.
	"""
	sync = []
	# positions = {
	# 	'stand': None,
	# 	'sit': None
	# }

	def __init__(self, data, servoType, wait=0.1):
		"""
		data: serial port to use, if none, then use dummy port
		kind: AX12 or XL320
		"""
		self.wait = wait
		# determine serial port
		# default to fake serial port
		if 'serialPort' in data:
			try:
				self.serial = ServoSerial(data['serialPort'])
				print('Using servo serial port: {}'.format(data['serialPort']))
				self.serial.open()

			except Exception as e:
				print(e)
				print('bye ...')
				exit(1)
		else:
			print('*** Using dummy serial port!!! ***')
			self.serial = ServoSerial('dummy')
			# raise Exception('No serial port given')

		self.packet = Packet(servoType)

		# for key in ['stand', 'sit']:
		# 	if key in data:
		# 		self.positions[key] = data[key]

	def pprint(self, i, step):
		print('***', i, '*'*25)
		for leg in step:
			print('  Servo: [{:.0f} {:.0f} {:.0f} {:.0f}]'.format(*leg))

	def setServoSpeed(self, speed):
		"""
		Sets the servo speed for all servos.
		speed - 0-1023, but only up to max speed of servo
		"""
		# make packet function
		pkt = self.packet.makeWritePacket(
			self.packet.base.BROADCAST_ADDR,
			self.packet.base.GOAL_VELOCITY,
			le(speed)
		)
		self.serial.write(pkt)

	# def moveLegsPosition2(self, legs):
	# 	"""
	# 	this only does position
	# 	[   step 0          step 1         ...
	# 		[[t1,t2,t3,t4], [t1,t2,t3,t4], ...] # leg0
	# 		[[t1,t2,t3,t4], [t1,t2,t3,t4], ...] # leg1
	# 		...
	# 	]
    #
	# 	FIXME: don't hard code for 4 legs, might want to just move 1 or 2 or 3
	# 	"""
	# 	# print('legs', legs, '\n\n')
	# 	# build sync message
	# 	# FIXME: hard coded for 4 legs
	# 	for j, step in enumerate(zip(*legs)):  # servo angles for each leg at each step
	# 		data = []  # [id, lo, hi, id, lo, hi, ...]
	# 		# leg 0: 0 1 2 3
	# 		# print('step', len(step), step, '\n')
	# 		self.pprint(j, step)
	# 		for i, leg in enumerate(step):  # step = [leg0, leg1, leg2, leg3]
	# 			# print('leg', len(leg), leg)
	# 			for j, servo in enumerate(leg):  # leg = [servo0, servo1, servo2, servo3]
	# 				s = []
	# 				s.append(4*i+j)      # servo ID
	# 				a, b = angle2int(servo)  # angle
	# 				s.append(a)
	# 				s.append(b)
	# 				data.append(s)
    #
	# 		# print('\n\ndata', data)
    #
	# 		pkt = self.packet.makeSyncWritePacket(self.packet.base.GOAL_POSITION, data)
	# 		self.serial.sendPkt(pkt)

	# FIXME: this also applies to non-gait movement ... moveLegs???
	def moveLegsGait(self, legs, speed=None):
		"""
		gait or sequence?
		speed = 1 - 1023 (scalar, all servos move at same rate)
		legs = { step 0        step 1         ...
			0: [[t1,t2,t3,t4], [t1,t2,t3,t4], ...] # leg0
			1: [[t1,t2,t3,t4], [t1,t2,t3,t4], ...] # leg1
			3: [[servo1, servo2, ...]] angles in servo space [0-300] deg
		}
		NOTE: each leg needs the same number of steps and servos per leg
		WARNING: these angles are in servo space [0-300 deg]
		"""
		# get the keys and figure out some stuff
		keys = list(legs.keys())
		numSteps = len(legs[keys[0]])
		numServos = len(legs[keys[0]][0])

		# print('steps', numSteps, 'servos', numServos)

		if speed:
			sl, sh = le(speed)
			wait = self.wait  # FIXME: wait should be a function of speed
		else:
			wait = self.wait

		# for each step in legs
		for s in range(numSteps):
			data = []
			for legNum in keys:
				step = legs[legNum][s]
				for i, a in enumerate(step):
					a, b = angle2int(a)  # angle
					if speed:
						data.append([legNum*numServos + i+1, a, b, sl, sh])  # ID, low angle, high angle, low speed, high speed
					else:
						data.append([legNum*numServos + i+1, a, b])  # ID, low angle, high angle

			# print('\n\ndata', data)

			pkt = self.packet.makeSyncWritePacket(self.packet.base.GOAL_POSITION, data)
			# print('raw pkt', pkt)
			self.serial.write(pkt)
			time.sleep(wait)

	# def moveLegsPosition(self, legs):
	# 	"""
	# 	[   step 0          step 1         ...
	# 		[[t1,t2,t3,t4], [t1,t2,t3,t4], ...] # leg0
	# 		[[t1,t2,t3,t4], [t1,t2,t3,t4], ...] # leg1
	# 		...
	# 	]
    #
	# 	FIXME: this moves angles from a gait, not position (x,y,z) ... rename or change interface to take points?
	# 	FIXME: don't hard code for 4 legs, might want to just move 1 or 2 or 3
	# 	FIXME: legs are positional ... can't just move leg 3, try:
	# 		legs = { here legs 1 and 4 are not moved
	# 			0: [t1,t2, ...], ... move leg 0
	# 			3: [t1, t2 ...], ... move leg 3
	# 		}
	# 	"""
	# 	# print('legs', legs, '\n\n')
	# 	# build sync message
	# 	# FIXME: hard coded for 4 legs
	# 	for g, step in enumerate(zip(*legs)):  # servo angles for each leg at each step
	# 		data = []  # [id, lo, hi, id, lo, hi, ...]
	# 		# leg 0: 0 1 2 3
	# 		# print('step', len(step), step, '\n')
	# 		self.pprint(g, step)
	# 		num_legs = len(step)
	# 		for i, leg in enumerate(step):  # step = [leg0, leg1, leg2, leg3]
	# 			# print('leg', len(leg), leg)
	# 			num_joints = len(leg)
	# 			for j, servo in enumerate(leg):  # leg = [servo0, servo1, servo2, servo3]
	# 				s = []
	# 				s.append(num_joints*i+j)      # servo ID
	# 				a, b = angle2int(servo)  # angle
	# 				s.append(a)
	# 				s.append(b)
	# 				data.append(s)
    #
	# 		# print('\n\ndata', data)
    #
	# 		pkt = self.packet.makeSyncWritePacket(self.packet.base.GOAL_POSITION, data)
	# 		self.serial.sendPkt(pkt)

	def moveLegsAnglesArray(self, angles, speed=None, degrees=True):
		"""
		The ID number is set by the array position
		speed = 1 - 1023 (scalar, all servos move at same rate)
		angles = [servo1, servo2, servo3 ...]
		WARNING: these angles are in servo space [0-300 deg]
		"""
		# print('legs', legs, '\n\n')
		# build sync message
		data = []
		if speed:
			sl, sh = le(speed)
		for i, a in enumerate(angles):
			a, b = angle2int(a)
			if speed:
				data.append([i+1, a, b, sl, sh])
			else:
				data.append([i+1, a, b])
		print('data', data)
		pkt = self.packet.makeSyncWritePacket(self.packet.base.GOAL_POSITION, data)

		# Status Packet will not be returned if Broadcast ID(0xFE) is used
		self.serial.write(pkt)  # no point to read
		# self.serial.sendPkt(pkt)
		print('moveLegsAnglesArray', pkt)

	# def stand(self):
	# 	if self.positions['stand']:
	# 		feet = {
	# 			0: [self.positions['stand']],
	# 			1: [self.positions['stand']],
	# 			2: [self.positions['stand']],
	# 			3: [self.positions['stand']],
	# 		}
	# 		self.moveLegsGait(feet, 100)
	# 		sleep(4)
	#
	# def sit(self):
	# 	if self.positions['sit']:
	# 		feet = {
	# 			0: [self.positions['sit']],
	# 			1: [self.positions['sit']],
	# 			2: [self.positions['sit']],
	# 			3: [self.positions['sit']],
	# 		}
	# 		self.moveLegsGait(feet, 100)
	# 		sleep(4)
