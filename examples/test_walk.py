#!/usr/bin/env python

from __future__ import print_function, division
from quadruped import Engine
from quadruped import DiscreteRippleGait
from math import pi
# import time


class Test(object):
	def __init__(self, data):
		self.robot = Engine(data)
		netural = self.robot.getFoot0(0)
		self.gaits = [DiscreteRippleGait(45.0, netural)]

	def run(self):
		# predefined walking path
		path = [  # x,y,rot
			# [1.0, 0, 0],
			# [1.0, 0, 0],
			# [1.0, 0, 0],
			# [1.0, 0, 0],
			# [1.0, 0, 0],
			# [1.0, 0, 0],
			# [1.0, 0, 0],
			# [1.0, 0, 0],
			# [1.0, 0, 0],
			# [1.0, 0, 0],
			[0, 0, pi/4],
			[0, 0, pi/4],
			[0, 0, pi/4],
			[0, 0, -pi/4],
			[0, 0, -pi/4],
			[0, 0, -pi/4],
			# [-1.0, 0, 0],
			# [-1.0, 0, 0],
			# [-1.0, 0, 0],
			# [-1.0, 0, 0],
			# [-1.0, 0, 0],
			# [-1.0, 0, 0],
			# [-1.0, 0, 0],
			# [-1.0, 0, 0],
			# [-1.0, 0, 0],
			# [-1.0, 0, 0],
		]

		crawl = self.gaits[0]

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

	test = Test(data)

	try:
		test.run()
	except KeyboardInterrupt:
		print('bye ...')
		time.sleep(1)


if __name__ == '__main__':
	main()
