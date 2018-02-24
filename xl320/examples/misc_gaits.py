from __future__ import print_function
from __future__ import division
# import numpy as np
# from math import cos, sin, sqrt, pi
from .Gait import Gait


class CircularGait(Gait):
	"""
	Raises one leg at a time and taps the legs in a circular pattern ... it does
	not walk, this is just for fun
	"""
	steps = 0

	def __init__(self, h, r, order=(0, 2, 1, 3)):
		Gait.__init__(self, r)
		self.order = order
		self.legOffset = [0, 3, 6, 9]
		# self.phi = [9/9, 6/9, 3/9, 0/9, 1/9, 2/9, 3/9, 4/9, 5/9, 6/9, 7/9, 8/9]  # foot pos in gait sequence
		maxl = h  # lifting higher gives me errors
		minl = maxl/2
		self.z = [minl, maxl, minl, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # leg height
		self.steps = len(self.z)
		self.foot_steps = self.pre_calc()

	def eachLeg(self, index):
		"""
		interpolates the foot position of each leg
		"""
		# if cmd is not None:
		# 	raise Exception("CircularGait::eachLeg cmd not None")

		# newpos = self.rest + np.array([0.0, 0.0, self.z[index]])
		newpos = [0]*3
		newpos[0] = self.rest[0] + 0.0
		newpos[1] = self.rest[1] + 0.0
		newpos[2] = self.rest[2] + self.z[index]

		# print('New  [](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(newpos[0], newpos[1], newpos[2]))
		return newpos

	def pre_calc(self):
		ret = []  # 4 leg foot positions for the entire 12 count cycle is returned

		for i in range(self.steps):  # iteration, there are 12 steps in gait cycle
			footPos = []
			print('-'*20)
			for legNum in self.order:  # order them diagonally
				index = (i + self.legOffset[legNum]) % self.steps
				pos = self.eachLeg(index)  # move each leg appropriately
				print('Foot[{}]: {:.2f} {:.2f} {:.2f}'.format(legNum, *(pos)))
				# if legNum == 0: print('New  [{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(i, pos[0], pos[1], pos[2]))
				footPos.append([index, legNum, pos])  # all in leg frame

			ret.append(footPos)  # 4 feet at index i: [index, legNum, footposition]
		return ret

	def oneCycle(self, x, y, rz):
		return self.foot_steps


class ImpatientGait(Gait):
	"""
	Raises one leg and taps its foot impatiently ... for fun
	"""
	steps = 0

	def __init__(self, h, r, order=(0,)):
		"""
		Does a tapping foot

		h - leg height
		r - resting/neutral foot position
		order - a tuple but it should only have 1 leg number in it
		"""
		Gait.__init__(self, r)
		self.order = order
		# self.phi = [9/9, 6/9, 3/9, 0/9, 1/9, 2/9, 3/9, 4/9, 5/9, 6/9, 7/9, 8/9]  # foot pos in gait sequence
		maxl = h  # lifting higher gives me errors
		minl = maxl/2
		self.z = [minl, maxl, minl, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # leg height
		self.steps = len(self.z)
		self.foot_steps = self.pre_calc()

	def eachLeg(self, index):
		"""
		interpolates the foot position of each leg
		"""
		# if cmd is not None:
		# 	raise Exception("CircularGait::eachLeg cmd not None")

		# rest = self.rest
		# i = index

		# create new move command
		# move = np.array([
		# 	0.0,
		# 	0.0,
		# 	self.z[i]
		# ])

		# new foot position: newpos = rot + move ----------------------------
		# newpos = move + rest
		newpos = [0]*3
		newpos[0] = self.rest[0] + 0.0
		newpos[1] = self.rest[1] + 0.0
		newpos[2] = self.rest[2] + self.z[index]

		# print('New  [](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(newpos[0], newpos[1], newpos[2]))
		return newpos

	def pre_calc(self):
		ret = []  # 4 leg foot positions for the entire 12 count cycle is returned

		for i in range(0, self.steps):  # iteration, there are 12 steps in gait cycle
			footPos = []
			for legNum in self.order:  # order them diagonally
				index = (i + self.legOffset[legNum]) % self.steps
				pos = self.eachLeg(index)  # move each leg appropriately
				footPos.append([index, legNum, pos])  # all in leg frame

			ret.append(footPos)  # 4 feet at index i: [index, legNum, footposition]

		return ret

	def oneCycle(self, x, y, rz):
		return self.foot_steps
