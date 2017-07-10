#!/usr/bin/env python
#
# by Kevin J. Walchko 26 Aug 2014
#
# PS4 has 6 axes, 14 buttons, 1 hat
# This program doesn't grab all buttons, just the most useful :)

# Warning: this code needs to be updated to support the new py2/py3 library. This
# may crash under py3 and hasn't been tested with the currentl pygecko library.

# https://github.com/chrippa/ds4drv


from __future__ import division
from __future__ import print_function

try:
	# brew install sdl2
	# pip install PySDL2
	import sdl2
except:
	print('You must install SLD2 library')
	exit()


class Joystick(object):
	"""
	Joystick class setup to handle a Playstation PS4 Controller. If no joystick
	is found, the self.valid is False. If it is not valid, the any returned
	dictionaries will contain all 0 values.

	Buttons
		Square  = joystick button 0
		X       = joystick button 1
		Circle  = joystick button 2
		Triangle= joystick button 3
		L1      = joystick button 4
		R1      = joystick button 5
		L2      = joystick button 6
		R2      = joystick button 7
		Share   = joystick button 8
		Options = joystick button 9
		L3      = joystick button 10
		R3      = joystick button 11
		PS      = joystick button 12
		PadPress= joystick button 13
	Axes:
		LeftStickX      = X-Axis
		LeftStickY      = Y-Axis (Inverted?)
		RightStickX     = 3rd Axis
		RightStickY     = 4th Axis (Inverted?)
		L2              = 5th Axis (-1.0f to 1.0f range, unpressed is -1.0f)
		R2              = 6th Axis (-1.0f to 1.0f range, unpressed is -1.0f)
		DPadX           = 7th Axis
		DPadY           = 8th Axis (Inverted?)
	WARNING: doesn't work as a process
	"""
	def __init__(self):
		# init SDL2 and grab joystick
		sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)
		self.js = sdl2.SDL_JoystickOpen(0)

		# grab info for display
		a = sdl2.SDL_JoystickNumAxes(self.js)
		b = sdl2.SDL_JoystickNumButtons(self.js)
		h = sdl2.SDL_JoystickNumHats(self.js)

		if a == -1:
			print('*** No Joystick found ***')
			self.valid = False
		else:
			print('==========================================')
			print(' PS4 Joystick ')
			print('   axes:', a, 'buttons:', b, 'hats:', h)
			print('==========================================')
			self.valid = True

		self.ps4 = {
			'num_axes': a,
			'num_buttons': b,
			'num_hats': h,
			'leftStick': [0, 0],
			'rightStick': [0, 0]
		}

	def __del__(self):
		# clean-up
		sdl2.SDL_JoystickClose(self.js)
		print('Bye ...')

	def get(self):
		ps4 = self.ps4
		js = self.js

		sdl2.SDL_JoystickUpdate()

		# left axis
		x = sdl2.SDL_JoystickGetAxis(js, 0) / 32768
		y = sdl2.SDL_JoystickGetAxis(js, 1) / 32768
		ps4['leftStick'] = [x, y]

		# right axis
		x = sdl2.SDL_JoystickGetAxis(js, 2) / 32768
		y = sdl2.SDL_JoystickGetAxis(js, 5) / 32768
		ps4['rightStick'] = [x, y]

		# # other axes
		# ps4.axes.L2 = sdl2.SDL_JoystickGetAxis(js, 3) / 32768
		# ps4.axes.R2 = sdl2.SDL_JoystickGetAxis(js, 4) / 32768
		#
		# # accels
		# x = sdl2.SDL_JoystickGetAxis(js, 6) / 32768
		# y = sdl2.SDL_JoystickGetAxis(js, 7) / 32768
		# z = sdl2.SDL_JoystickGetAxis(js, 8) / 32768
		# ps4.axes.accels = [x, y, z]
		#
		# # gyros
		# x = sdl2.SDL_JoystickGetAxis(js, 9) / 32768
		# y = sdl2.SDL_JoystickGetAxis(js, 10) / 32768
		# z = sdl2.SDL_JoystickGetAxis(js, 11) / 32768
		# ps4.axes.gyros = [x, y, z]
		#
		# # get buttons
		# ps4.buttons.s = sdl2.SDL_JoystickGetButton(js, 0)
		# ps4.buttons.x = sdl2.SDL_JoystickGetButton(js, 1)
		# ps4.buttons.o = sdl2.SDL_JoystickGetButton(js, 2)
		# ps4.buttons.t = sdl2.SDL_JoystickGetButton(js, 3)
		# ps4.buttons.L1 = sdl2.SDL_JoystickGetButton(js, 4)
		# ps4.buttons.R1 = sdl2.SDL_JoystickGetButton(js, 5)
		# ps4.buttons.L2 = sdl2.SDL_JoystickGetButton(js, 6)
		# ps4.buttons.R2 = sdl2.SDL_JoystickGetButton(js, 7)
		# ps4.buttons.share = sdl2.SDL_JoystickGetButton(js, 8)
		# ps4.buttons.options = sdl2.SDL_JoystickGetButton(js, 9)
		# ps4.buttons.L3 = sdl2.SDL_JoystickGetButton(js, 10)
		# ps4.buttons.R3 = sdl2.SDL_JoystickGetButton(js, 11)
		# ps4.buttons.ps = sdl2.SDL_JoystickGetButton(js, 12)
		# ps4.buttons.pad = sdl2.SDL_JoystickGetButton(js, 13)
		#
		# # get hat
		# # [up right down left] = [1 2 4 8]
		# ps4.buttons.hat = sdl2.SDL_JoystickGetHat(js, 0)

		# print('b 12', sdl2.SDL_JoystickGetButton(js, 12))
		# print('b 13', sdl2.SDL_JoystickGetButton(js, 13))

		# if verbose:  # print(Msg.Joystick.screen(ps4))
		# 	print(ps4.axes.accels)

		# except (IOError, EOFError):
		# 	print('[-] Connection gone .... bye')
		# 	break
		#
		# except (KeyboardInterrupt, SystemExit):
		# 	print('js bye ...')
		# 	break
		# except Exception as e:
		# 	print('Ooops:', e)
		# else:
		# 	raise Exception('Joystick: Something bad happened!')
		return ps4


def main():
	import time

	js = Joystick()

	while True:
		try:
			ps4 = js.get()
			print(ps4)
			time.sleep(1)
		except KeyboardInterrupt:
			print('js exiting ...')


if __name__ == "__main__":
	main()
