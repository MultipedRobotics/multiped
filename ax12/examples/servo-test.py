# #!/usr/bin/env python
# ##############################################
# # The MIT License (MIT)
# # Copyright (c) 2018 Kevin Walchko
# # see LICENSE for full details
# ##############################################
#
# from __future__ import print_function
# from __future__ import division
# # from quadruped import Engine
# # from quadruped import DiscreteRippleGait
# from quadruped import Servo
# # from quadruped import Leg4
# from pyservos import AX12
# import time
#
#
# class ServoTest(object):
# 	def __init__(self, ID, offset=150):
# 		self.servo = Servo(ID, AX12)
# 		self.servo.setNewSerial('/dev/tty.usbserial-A506BOT5')
# 		self.servo.setServoLimits(offset, -110, 110)
#
# 	def array(self):
# 		for a in [-90, -45, 0, 45, 90, 0]:
# 			self.servo.angle = a
# 			time.sleep(2)
#
# 	def single(self, a=0):
# 		self.servo.angle = a
# 		time.sleep(2)
#
#
# def main():
# 	test = ServoTest(4)
#
# 	try:
# 		test.array()
# 		# test.single()
# 	except KeyboardInterrupt:
# 		print('bye ...')
# 		time.sleep(1)
#
#
# if __name__ == '__main__':
# 	main()
