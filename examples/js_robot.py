#!/usr/bin/env python

##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################
# Simple robot that you can drive with a PS4 joystick
#
# It is meant to run on a raspberry pi and if linux isn't detected, then some
# sensors are not loaded.

from __future__ import print_function
from __future__ import division
from quadruped import Engine
from quadruped import DiscreteRippleGait
from quadruped import Robot
from js import Joystick
from misc_gaits import CircularGait, ImpatientGait
import platform
import time
##########################


class SimpleQuadruped(Robot):
	"""
	This uses the Robot base class from quadruped
	"""

	def __init__(self, data):
		"""
		Constructor.
		js - joystick (works on linux and macOS)
		"""
		Robot.__init__(self, data)
		self.js = Joystick()

	def run(self):
		"""
		A loop that doesn't end and allows you to drive the robot
		"""
		while True:
			if self.js.valid:
				ps4 = self.js.get()
				x, y = ps4['leftStick']
				rz, _ = ps4['rightStick']
				cmd = (x, y, rz)
			else:
				cmd = (1, 0, 0)

			print('***********************************')
			print('* cmd {:.2f} {:.2f} {:.2f}'.format(*cmd))

			mov = self.gait['impatient_tap'].command(cmd)
			if mov:
				self.robot.move(mov)
			else:
				time.sleep(1)


def run():
	# bulk - use bulk or sync writing on the xl-320 servos
	# uncomment and change the serial port as necessary
	test = {
		'serialPort': '/dev/tty.usbserial-AL034G2K',  # sparkfun usb-serial
		'write': 'bulk'
	}

	robot = SimpleQuadruped(test)

	try:
		robot.run()

	except KeyboardInterrupt:
		print('bye ...')


if __name__ == "__main__":
	run()
