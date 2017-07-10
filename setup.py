from __future__ import print_function
from setuptools import setup
from quadruped.version import __version__ as VERSION
from build_utils import BuildCommand
from build_utils import PublishCommand
from build_utils import BinaryDistribution


PACKAGE_NAME = 'quadruped'
BuildCommand.pkg = PACKAGE_NAME
PublishCommand.pkg = PACKAGE_NAME
PublishCommand.version = VERSION
README = open('README.rst').read()

setup(
	name=PACKAGE_NAME,
	version=VERSION,
	author="Kevin Walchko",
	keywords=['framework', 'robotic', 'robot', 'sdl2', 'ps4', 'quadruped'],
	author_email="walchko@users.noreply.github.com",
	description="A python robotic driver for a quadruped robot",
	license="MIT",
	classifiers=[
		'Development Status :: 4 - Beta',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3.6',
		'Operating System :: Unix',
		'Operating System :: POSIX :: Linux',
		'Operating System :: MacOS :: MacOS X',
		'Operating System :: POSIX',
		'Topic :: Scientific/Engineering',
		'Topic :: Scientific/Engineering :: Artificial Intelligence',
		# 'Topic :: Scientific/Engineering :: Image Recognition',
		'Topic :: Software Development :: Libraries :: Python Modules'
	],
	install_requires=[
		'nxp_imu',
		'pyxl320',
		'simplejson',
		'pyserial',
		'numpy',
		'build_utils',
		'mcp3208'
	],
	url="https://github.com/MomsFriendlyRobotCompany/{}".format(PACKAGE_NAME),
	long_description=README,
	packages=[PACKAGE_NAME],
	cmdclass={
		'publish': PublishCommand,
		'make': BuildCommand
	},
	scripts=[
		'bin/get_leg_info.py',
		'bin/get_leg_angles.py'
	]
)
