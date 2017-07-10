#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
import simplejson as json


class FileStorageError(Exception):
	pass


class jsonFile(object):
	"""
	Store your API keys or other params in a json/yaml file and then import them
	with this class. You can also pass a dictionary to this and create a json/yaml
	file storage. All key/value pairs are stored in a dictionary called db.
	"""
	db = None

	def read(self, fname):
		"""
		Reads a Json file
		in: file name
		out: length of file, dictionary
		"""
		try:
			with open(fname, 'r') as f:
				data = json.load(f)

			self.db = data
			return len(self.db), data
		except IOError:
			raise FileStorageError('Could not open {0!s} for reading'.format((fname)))

	def write(self, fname, data=None):
		"""
		Writes a Json file
		"""
		try:
			if data is None:
				data = self.db

			with open(fname, 'w') as f:
				json.dump(data, f)

		except IOError:
			raise FileStorageError('Could not open {0!s} for writing'.format((fname)))

	def __getitem__(self, keyName):
		if keyName in self.db:
			return self.db[keyName]
		else:
			return None

	def __str__(self):
		s = []
		for k, v in db.items():
			s.append(str(k) + ': ' + str(v) + '\n')
		return ''.join(s)

	def __repr__(self):
		print(self.__str__())

	def clear(self):
		self.db = None


if __name__ == '__main__':
	fs = jsonFile()
	fs.read('walkingeye.json')
	db = fs.db

	print('serialPort', fs['serialPort'])
	print('')

	print(fs)
