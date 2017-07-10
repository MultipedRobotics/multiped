
.. image:: https://raw.githubusercontent.com/walchko/quadruped/master/pics/spiderbot_dev.JPG
	:target: https://github.com/MomsFriendlyRobotCompany/quadruped

Quadruped
============================

.. image:: https://img.shields.io/pypi/v/quadruped.svg
	:target: https://github.com/MomsFriendlyRobotCompany/quadruped
.. image:: https://img.shields.io/pypi/l/quadruped.svg
	:target: https://github.com/MomsFriendlyRobotCompany/quadruped
.. image:: https://travis-ci.org/MomsFriendlyRobotCompany/quadruped.svg?branch=master
	:target: https://travis-ci.org/MomsFriendlyRobotCompany/quadruped

My robot software.

Documentation
-------------------

**Note:** This re-write is still very early and not fully running yet, just
parts.

The documentation can be found `here <docs/Markdown>`_.


Install
-----------

pip
~~~~~

The recommended way to install this library is::

	pip install quadruped

Development
~~~~~~~~~~~~~

If you wish to develop and submit git-pulls, you can do::

	git clone https://github.com/MomsFriendlyRobotCompany/quadruped
	cd quadruped
	pip install -e .

Testing
~~~~~~~~~

Since I have both python2 and python3 installed, I need to test with both::

	python2 -m nose *.py
	python3 -m nose *.py

Layout
------------

Here is *sort* of the layout of the code:

- Quadruped (*see examples folders*):
	- Engine(serial)
	- AHRS() - tilt compensated compass
	- IMU() - NXP IMU from Adafruit
	- MCP3208() - ADC for IR and whatever else
	- Gait:
		- command() - plans all feet through 1 gait cycle (12 steps)
		- eachLeg(x,y,z)

- Engine({serial}): - handles movement hardware
	- legs[4]
		- servos[3]
			- angle
			- setServoLimits()
			- bulkWrite() - change to sync
		- coxa, femur, tibia
		- fk()
		- ik()
		- moveFoot(x,y,z)
		- moveFootAngle(a,b,c)

The example quadruped (in the examples folder), takes a dictionary. Currently
it takes::

	data = {
		'serialPort': '/dev/tty.usbserial-AL034G2K',
		'write': 'bulk'
	}

If you don't pass it a serial port, then it falls back to a simulated serial
port (which does nothing) which is useful for testing.

Tools
---------

This directory contains several tools for the robot:

Change Log
-------------

============ ======= ============================
2017-Jul-07  0.4.1   broke out into package and published to PyPi
2016-Aug-10  0.0.1   init
============ ======= ============================


MIT License
---------------

**Copyright (c) 2016 Kevin J. Walchko**

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
