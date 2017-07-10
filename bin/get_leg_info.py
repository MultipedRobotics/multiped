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
from serial import SerialException
import sys
from packetDecoder import PacketDecoder


def writeToFile(data, filename='data.json'):
	with open(filename, 'w') as outfile:
		json.dump(data, outfile)


def pktToDict(p):
	# print('pkt', pkt)
	# print('len(pkt)', len(pkt))
	ans = {}
	ans['ID'] = p.id
	ans['Present Position'] = p.angle()
	ans['Present Voltage'] = p.voltage()
	ans['Present Load'] = '{:>5.1f}% {}'.format(*p.load())
	ans['Present Temperature'] = p.temperature(PacketDecoder.F)
	ans['Hardware Error Status'] = p.hw_error()

	return ans


DESCRIPTION = """
Returns limited info for each leg servo.

./get_leg_info.py /dev/tty.usbserial-AL034G2K
Opened /dev/tty.usbserial-AL034G2K @ 1000000

Servos: 1 - 12
--------------------------------------------------
Servo: 1  		HW Error: 0
Position [deg]: 139.6  Load:   0.0% CCW
Voltage [V]  7.0     Temperature [F]:  80.6
--------------------------------------------------
Servo: 2  		HW Error: 0
Position [deg]: 178.9  Load:   4.5% CW
Voltage [V]  7.1     Temperature [F]:  86.0
--------------------------------------------------
Servo: 3  		HW Error: 0
Position [deg]: 119.1  Load:   0.0% CCW
Voltage [V]  7.1     Temperature [F]:  80.6
--------------------------------------------------
Servo: 4  		HW Error: 0
Position [deg]: 146.6  Load:   0.8% CCW
Voltage [V]  7.3     Temperature [F]:  80.6
--------------------------------------------------
Servo: 5  		HW Error: 0
Position [deg]: 275.4  Load:   0.8% CCW
Voltage [V]  7.1     Temperature [F]:  80.6
--------------------------------------------------
Servo: 6  		HW Error: 0
Position [deg]: 104.1  Load:   0.0% CCW
Voltage [V]  7.3     Temperature [F]:  82.4
--------------------------------------------------
Servo: 7  		HW Error: 0
Position [deg]: 163.9  Load:   0.0% CCW
Voltage [V]  7.2     Temperature [F]:  80.6
--------------------------------------------------
Servo: 8  		HW Error: 0
Position [deg]: 279.5  Load:   0.0% CCW
Voltage [V]  7.1     Temperature [F]:  80.6
--------------------------------------------------
Servo: 9  		HW Error: 0
Position [deg]: 100.3  Load:   0.0% CCW
Voltage [V]  7.1     Temperature [F]:  84.2
--------------------------------------------------
Servo: 10  		HW Error: 0
Position [deg]: 156.3  Load:   0.0% CCW
Voltage [V]  7.1     Temperature [F]:  82.4
--------------------------------------------------
Servo: 11  		HW Error: 0
Position [deg]: 280.6  Load:   0.0% CCW
Voltage [V]  7.2     Temperature [F]:  80.6
--------------------------------------------------
Servo: 12  		HW Error: 0
Position [deg]:  97.7  Load:   0.0% CCW
Voltage [V]  7.1     Temperature [F]:  84.2
--------------------------------------------------
"""


def handleArgs():
	parser = argparse.ArgumentParser(description=DESCRIPTION, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('port', help='serial port  or \'dummy\' for testing', type=str)
	parser.add_argument('-j', '--json', metavar='FILENAME', help='save info to a json file: --json my_file.json', type=str)

	args = vars(parser.parse_args())
	return args


def getSingle(ID, ser):
	pkt = makeReadPacket(ID, 37, le(50-37+1))
	# print('made packet:', pkt)

	ans = ser.sendPkt(pkt)
	if ans:
		ans = ans[0]
		pd = PacketDecoder(ans, 37)  # data packet starts at register 37
		# pd.printPacket()
		if pd.checkError():
			raise Exception('Crap!')
		ans = pktToDict(pd)
	else:
		ans = None

	return ans


def printServo(s):
	print('-'*50)
	print('Servo: {}  \t\tHW Error: {}'.format(s['ID'], s['Hardware Error Status']))
	print('Position [deg]: {:5.1f}  Load: {}'.format(s['Present Position'], s['Present Load']))
	print('Voltage [V] {:4.1f}     Temperature [F]: {:5.1f}'.format(s['Present Voltage'], s['Present Temperature']))


def main():
	args = handleArgs()
	port = args['port']

	s = ServoSerial(port=port)

	# open serial port
	try:
		s.open()
	except SerialException as e:
		print('-'*20)
		print(sys.argv[0], 'encountered an error')
		print(e)
		exit(1)

	ids = range(1, 13)

	resp = {}
	for k in ids:
		resp[k] = None

	# get servo data
	try:
		for i in ids:
			data = getSingle(i, s)
			resp[i] = data
	except Exception as e:
		print(e)
		exit(1)

	cnt = 10
	while cnt:
		cnt = 0
		for k, v in resp.items():
			# search through and find servos w/o responses (i.e., None)
			if v is None:
				cnt += 1  # found a None
				ans = getSingle(k, s)
				resp[k] = ans

	print('')
	print('Servos: 1 - 12')
	for i in range(1, 13):
		printServo(resp[i])
	print('-' * 50)
	print('')

	if args['json']:
		print('Saving servo angle info to {}'.format(args['json']))
		writeToFile(resp, args['json'])

	s.close()


if __name__ == '__main__':
	main()
