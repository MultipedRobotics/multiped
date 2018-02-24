#!/usr/bin/env python

from __future__ import print_function, division
from quadruped import Engine
from quadruped import DiscreteRippleGait
from quadruped import Robot
from misc_gaits import CircularGait, ImpatientGait
from math import pi
import time


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
		crawl = self.gaits['crawl']
		# crawl = self.gaits['circle_tap']
		# crawl = self.gaits['impatient_tap']

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
		#'serialPort': '/dev/tty.usbserial-AL034G2K',  # sparkfun usb-serial
		'serialPort': '/dev/ttyUSB0',
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
