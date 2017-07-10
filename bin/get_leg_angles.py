#!/usr/bin/env python

##############################################
# The MIT License (MIT)
# Copyright (c) 2017 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function, division
from pyxl320 import ServoSerial
from pyxl320.Packet import le, makeReadPacket
import argparse
import simplejson as json


def writeToFile(data, filename='data.json'):
	with open(filename, 'w') as outfile:
		json.dump(data, outfile)


DESCRIPTION = """
Returns the angles of servos
"""


def handleArgs():
	parser = argparse.ArgumentParser(description=DESCRIPTION, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('port', help='serial port  or \'dummy\' for testing', type=str)
	parser.add_argument('-j', '--json', help='save info to a json file, you must supply a file name: --json my_file.json', type=str)

	args = vars(parser.parse_args())
	return args


def getInfo(pkt):
	ID = pkt[4]
	angle = float((pkt[10] << 8) + pkt[9])/1023
	angle *= 300.0
	return ID, angle


def getSingle(ID, ser):
	pkt = makeReadPacket(ID, 37, le(2))
	# print('made packet:', pkt)
	ID = None
	angle = None

	ans = ser.sendPkt(pkt)
	if ans:
		ans = ans[0]
		ID, angle = getInfo(ans)

	return ID, angle


def main():
	args = handleArgs()
	port = args['port']

	s = ServoSerial(port=port)
	s.open()

	ids = range(1, 13)

	resp = {}
	for k in ids:
		resp[k] = None

	# as more servos add up, I might need to increase the cnt number???
	for i in ids:
		ID, angle = getSingle(i, s)
		resp[i] = angle

	cnt = 10
	while cnt:
		cnt = 0
		for k, v in resp.items():
			# search through and find servos w/o responses (i.e., None)
			if v is None:
				cnt += 1  # found a None
				ID, angle = getSingle(k, s)
				resp[k] = angle

	print('')
	print('Servos: 1 - 12')
	print('All angles are in {}'.format('degrees'))
	print(' {:>13} | {:>13} | {:>13} | {:>13} |'.format('Leg 1', 'Leg 2', 'Leg 3', 'Leg 4'))
	print(' {:>4} | {:6} | {:>4} | {:6} | {:>4} | {:6} | {:>4} | {:6} |'.format('ID', 'Angle', 'ID', 'Angle', 'ID', 'Angle', 'ID', 'Angle'))
	print('-' * 65)
	# for k, v in resp.items():
	# 	if v is None:
	# 		print('{:4} | {}'.format(k, 'unknown'))
	# 	else:
	# 		print('{:4} | {:6.2f}'.format(k, v))
	for i in range(1, 4):
		print(' {:4} | {:6.2f} | {:4} | {:6.2f} | {:4} | {:6.2f} | {:4} | {:6.2f}'.format(i, resp[i], i+3, resp[i+3], i+6, resp[i+6], i+9, resp[i+9]))
	print('-' * 65)
	print('')

	if args['json']:
		print('Saving servo angle info to {}'.format(args['json']))
		writeToFile(resp, args['json'])

	s.close()


if __name__ == '__main__':
	main()
