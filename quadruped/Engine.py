#!/usr/bin/env python

##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
from .Leg import Leg
from pyxl320 import ServoSerial
# from pyxl320 import DummySerial
from .Servo import Servo
from pyxl320 import Packet
from pyxl320 import xl320
import time


class Engine(object):
	"""
	change name to Hardware???

	This is the low level driver that can be executed w/o using pyGecko.
	"""
	def __init__(self, data={}):
		"""
		Sets up all 4 legs and servos. Also setups limits for angles and servo
		pulses.
		"""
		if 'serialPort' in data:
			try:
				ser = ServoSerial(data['serialPort'])
				print('Using servo serial port: {}'.format(data['serialPort']))

			except:
				print('bye ...')
				exit(1)
		else:
			print('Using dummy serial port!!!')
			ser = ServoSerial('test_port', fake=True)
			# raise Exception('No serial port given')

		ser.open()
		Servo.ser = ser  # set static serial port, not sure I like this

		if 'write' in data:
			method = data['write']
			if method == 'sync':
				Servo.syncServoWrite = True  # FIXME: this is broken
				print('*** using sync write ***')
			elif method == 'bulk':
				Servo.bulkServoWrite = True
				print('*** using bulk write ***')

		self.legs = []
		for i in range(0, 4):  # 4 legs
			channel = i*3  # 3 servos per leg
			self.legs.append(
				Leg([channel+1, channel+2, channel+3])
			)

		# better way?????
		self.servoWrite = self.legs[0].servos[0].write

		self.stand()

	def __del__(self):
		"""
		Leg kills (reboots) all servos on exit.

		Eventually will put the robot in sit pose.
		"""
		self.sit()
		pkt = Packet.makeRebootPacket(xl320.XL320_BROADCAST_ADDR)
		Servo.ser.write(pkt)
		Servo.ser.write(pkt)
		time.sleep(0.1)
		Servo.ser.close()  # close static serial port

	def sit(self):
		"""
		sequence to sit down nicely
		"""
		for leg in self.legs:
			leg.sit()
		self.servoWrite()  # FIXME: ugly
		time.sleep(1)

	def stand(self):
		"""
		sequence to stand up nicely
		"""
		for leg in self.legs:
			leg.stand()
		self.servoWrite()  # FIXME: ugly
		time.sleep(1)

	def getFoot0(self, i):
		"""
		rename getNeutral?
		"""
		return self.legs[i].foot0

	def move(self, cycle):
		"""
		cycle - move of 4 legs through all steps
		"""
		for mov in cycle:
			for leg in mov:
				index = leg[1]
				footPos = leg[2]
				# print('Leg[{}]: {}'.format(index, footPos))
				self.legs[index].moveFoot(*footPos)
			self.servoWrite()  # FIXME: ugly
			time.sleep(0.1)
