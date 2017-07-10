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
from js import Joystick
from nxp_imu import IMU
import platform
import time
# from ahrs import AHRS  # attitude and heading reference system
##########################


class SimpleQuadruped(object):
	def __init__(self, data):
		"""
		Constructor.
		Engine - commands the leg servos to move
		gait - Ideally there are several types of gaits for different
		       walking/running situations. The gaits need to know:
		       - how high to pick up a leg
		       - what the neutral leg position is (where is the foot
		         located when just standing?)
		js - joystick (works on linux and macOS)
		imu - inertial measurement unit (must be on linux)
		"""
		self.robot = Engine(data)
		netural = self.robot.getFoot0(0)
		self.gait = {
			'crawl': DiscreteRippleGait(45.0, netural)
		}
		if platform.system() == 'Linux':
			self.imu = IMU()
		else:
			self.imu = None

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

			# read ahrs
			if self.imu:
				a, m, g = self.imu.read()
				# roll, pitch, heading = d
				# if (-90.0 > roll > 90.0) or (-90.0 > pitch > 90.0):
				# 	print('Crap we flipped!!!')
				# 	cmd = (0, 0, 0)
				print('imu', a, m, g)

			print('***********************************')
			# print('* rest {:.2f} {:.2f} {:.2f}'.format(*leg))
			# print('ahrs[deg]: roll {:.2f} pitch: {:.2f} yaw: {:.2f}'.format(d[0], d[1], d[2]))
			print('* cmd {:.2f} {:.2f} {:.2f}'.format(*cmd))
			# print('***********************************')
			mov = self.gait['crawl'].command(cmd)
			if mov:
				self.robot.move(mov)
			else:
				time.sleep(1)


def run():
	# bulk - use bulk or sync writing on the xl-320 servos
	# uncomment and change the serial port as necessary
	test = {
		# 'serialPort': '/dev/tty.usbserial-AL034G2K',  # sparkfun usb-serial
		'write': 'bulk'
	}

	robot = SimpleQuadruped(test)

	try:
		robot.run()

	except KeyboardInterrupt:
		print('bye ...')


if __name__ == "__main__":
	run()
