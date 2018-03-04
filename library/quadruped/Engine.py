##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
from pyservos import ServoSerial
from pyservos import Packet
from pyservos import AX12
from pyservos.packet import angle2int
# import time


class Engine(object):
	sync = []

	def __init__(self, data, servoType):
		"""
		data: serial port to use, if none, then use dummy port
		kind: AX12 or XL320
		"""
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

		self.packet = Packet(servoType)

	def pprint(self, i, step):
		print('***', i, '*'*25)
		for leg in step:
			print('  Servo: [{:.0f} {:.0f} {:.0f} {:.0f}]'.format(*leg))

	def moveLegsPosition(self, legs):
		"""
		this only does position
		[   step 0          step 1         ...
			[[t1,t2,t3,t4], [t1,t2,t3,t4], ...] # leg0
			[[t1,t2,t3,t4], [t1,t2,t3,t4], ...] # leg1
			...
		]
		"""
		# print('legs', legs, '\n\n')
		# build bulk message
		# FIXME: hard coded for 4 legs
		for j, step in enumerate(zip(*legs)):  # servo angles for each leg at each step
			data = []  # [id, lo, hi, id, lo, hi, ...]
			# leg 0: 0 1 2 3
			# print('step', len(step), step, '\n')
			self.pprint(j, step)
			for i, leg in enumerate(step):  # step = [leg0, leg1, leg2, leg3]
				# print('leg', len(leg), leg)
				for j, servo in enumerate(leg):  # leg = [servo0, servo1, servo2, servo3]
					s = []
					s.append(4*i+j)      # servo ID
					a, b = angle2int(servo)  # angle
					s.append(a)
					s.append(b)
					data.append(s)

			# print('\n\ndata', data)

			# FIXME: hard coded to AX
			pkt = self.packet.makeSyncWritePacket(AX12.GOAL_POSITION, data)
			self.serial.sendPkt(pkt)
			# time.sleep(.3)
