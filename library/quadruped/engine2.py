




class Servo(object):
	_angle = 0.0  # current angle
	_offset = 150.0  # angle offset default, see above for explaination
	minAngle = -150.0
	maxAngle = 150.0
	ID = 0

	def __init__(self, ID, min, max, offset):
		pass

	@property
	def angle(self):
		"""
		Returns the current servo angle
		"""
		return self._angle

	@angle.setter
	def angle(self, angle):
		pass


class Engine(object):
	sync = []

	def __init__(self, kind):
		self.serial = ServoSerial('/dev/tty.usbserial')  # tell it what port you want to use
		# serial = ServoSerial('dummy')  # use a dummy serial interface for testing
		self.serial.open()

		self.packet = Packet(kind)
		# pkt = ax.makeServoPacket(1, 158.6)  # move servo 1 to 158.6 degrees

		# angle offsets to line up with fk
		self.servos = []
		for i in range(0, 4):
			self.servos.append(Servo(channels[i]))
			self.servos[i].setServoLimits(self.s_offsets[i], *self.s_limits[i])

	def push(self, ID, angle, speed=None):
		self.sync.append((ID, angle))

	def write(self):
		# use self.sync to build packet

		ret = serial.sendPkt(pkt)
		# ret = serial.sendPkt(pkt)
