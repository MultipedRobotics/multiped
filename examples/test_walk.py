#!/usr/bin/env python

from __future__ import print_function, division
from quadruped import Engine
from quadruped import DiscreteRippleGait
from quadruped.misc_gaits import CircularGait, ImpatientGait
from math import pi
import time

# sensor robot -------
from nxp_imu import IMU
from mcp3208 import MCP3208
# from ins_nav import AHRS
import platform


class Robot(object):
	def __init__(self, data, gaits=None):
		"""
		Constructor.

		This enables the basic parts of the quadruped required for walking.
		Engine: commands the leg servos to move acording to a gait sequence
		gaits: Ideally there are several types of gaits for different
		       walking/running situations. The gaits need to know:
		       - how high to pick up a leg
		       - what the neutral leg position is (where is the foot
		         located when just standing?)
		"""
		self.robot = Engine(data)
		neutral = self.robot.getFoot0(0)

		if gaits is None:
			self.gaits = {
				'crawl': DiscreteRippleGait(45.0, neutral)
			}
		else:
			for k, v in gaits.items():
				self.gaits[k] = v(45.0, neutral)


class SensorRobot(Robot):
	def __init__(self, data):
		Robot.__init__(self, data)
		if platform.system() == 'Linux':
			self.imu = IMU()
			self.adc = MCP3208()

		# self.js = Joystick()
		# self.ahrs = AHRS()


class Test(Robot):
	def __init__(self, data, gaits):
		Robot.__init__(self, data, gaits)

	def run(self):
		# predefined walking path
		# x, y, rotation
		path = [
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[0, 0, pi/4],
			[0, 0, pi/4],
			[0, 0, pi/4],
			[0, 0, -pi/4],
			[0, 0, -pi/4],
			[0, 0, -pi/4],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
		]

		# pick a gait to use
		# crawl = self.gaits['crawl']
		# crawl = self.gaits['circle_tap']
		crawl = self.gaits['impatient_tap']

		for cmd in path:

			print('***********************************')
			# print(' rest {:.2f} {:.2f} {:.2f}'.format(*leg))
			# print('ahrs[deg]: roll {:.2f} pitch: {:.2f} yaw: {:.2f}'.format(d[0], d[1], d[2]))
			print(' cmd {:.2f} {:.2f} {:.2f}'.format(*cmd))
			# print('***********************************')
			mov = crawl.command(cmd)
			self.robot.move(mov)


def main():
	data = {
		'serialPort': '/dev/tty.usbserial-AL034G2K',  # sparkfun usb-serial
		'write': 'bulk'
	}

	gaits = {
		'crawl': DiscreteRippleGait,
		'circle_tap': CircularGait,
		'impatient_tap': ImpatientGait
	}

	test = Test(data, gaits)

	try:
		test.run()
	except KeyboardInterrupt:
		print('bye ...')
		time.sleep(1)


if __name__ == '__main__':
	main()
