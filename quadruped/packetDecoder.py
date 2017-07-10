from __future__ import print_function, division
from pyxl320.xl320 import ErrorStatusMsg


class PacketDecoder(object):
	"""
	move to pyxl320.Packet?

	Given a packet (array of integers) from the servo, decode it.

	ToDo:
		- finish decoding all register info
	"""
	F = 0
	C = 1

	def __init__(self, pkt, offset=0):
		self.id = pkt[4]  # save servo ID
		self.instr = pkt[7]  # should be 0x55 (85) for status packet
		self.len = self.get16b(pkt[5], pkt[6]) - 4  # don't count: instr, error, crc[0,1]
		self.pkt = pkt[9:-2]  # remove header, crc, and other stuff ... keep only data section
		self.offset = offset
		self.error = pkt[8]  # should be 0 if all is well

	def checkError(self):
		"""
		Does the return status packet say there is an error?

		return:
			True: there is an error and prints info to std out
			False: all is good with the world ... turtles all the way down
		"""
		if self.instr == 0x55:
			if self.error == 0x00:
				return False
			else:
				print('Servo[{}]: {}'.format(self.id, ErrorStatusMsg[self.error]))
				return True
		else:
			print('Servo[{}]: did not give a status message'.format(self.id))
			return True
		return True

	@staticmethod
	def get16b(lo, hi):
		return ((hi << 8) + lo)

	def getBase(self, reg):
		base = reg - self.offset
		# print('base', base)

		if base < 0:
			raise Exception('PacketDecoder::base < 0')

		if base >= self.len:
			raise Exception('PacketDecoder::packet not long enough to access this packet')

		return base

	def voltage(self):
		base = self.getBase(45)
		return self.pkt[base]/10

	def angle(self):
		base = self.getBase(37)
		return self.get16b(self.pkt[base], self.pkt[base+1])/1023 * 300.0

	def load(self):
		base = self.getBase(41)
		load = self.get16b(self.pkt[base], self.pkt[base+1])
		direction = 'CW' if (load & 1024) == 1024 else 'CCW'
		percent = (load & 1023)/1023 * 100
		return percent, direction

	def temperature(self, scale=0):
		base = self.getBase(46)
		temp = 0.0
		if scale == self.F:
			temp = self.pkt[base]*9/5+32
		else:
			temp = self.pkt[base]*1.0
		return temp

	def hw_error(self):
		base = self.getBase(50)
		return self.pkt[base]

	def printPacket(self):
		"""
		"""
		print('-'*70)
		print('Servo[{}]  instr: {}  error: {}  len(data): {}'.format(self.id, self.instr, self.error, self.len))
		print('raw:', self.pkt)
