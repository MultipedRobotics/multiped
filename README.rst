
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

* `YouTube <https://www.youtube.com/watch?v=kH2hlxUfCNg>`_
* `Vimeo <https://player.vimeo.com/video/194676675>`_

Documentation
-------------------

**Note:** This re-write is still very early and not fully running yet, just
parts.

Install
-----------

linux
~~~~~~~~

You will also need::

	pip install ds4drv

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

- SimpleQuadruped(data) (*see examples folders*):
	- class members
		- imu: inertial measurement unit
		- adc: analog to digital controller
		- ir: an array of ir sensor readings
		- ahrs: tilt compensated compass
		- js: joystick input
		- camera: pi camera
	- class methods:
		- Engine
		- Gait
- Gait:
	- Gait calculates the foot positions for 1 cycle of a movement
	- command() - plans all feet through 1 gait cycle (12 steps)
	- eachLeg(x,y,z)
	
- Engine:
	- Engine takes the output from Gait and calculates the servo joint positions
	  for each time stop and each leg in the cycle. It then sends the command to
	  move the servos at the end of the time step.
	- legs[4]
		- servos[3]
			- angle
			- setServoLimits()
			- bulkWrite()
			- syncWrite()
		- coxa, femur, tibia
		- fk() - forward kinematics
		- ik() - inverse kinematics
		- moveFoot(x,y,z) - for inverse kinematics
		- moveFootAngle(a,b,c) - for forward kinematics

The example quadruped (in the examples folder), takes a dictionary. Currently
it takes::

	data = {
		'serialPort': '/dev/tty.usbserial-AL034G2K',
		'write': 'bulk'
	}

If you don't pass it a serial port, then it falls back to a simulated serial
port (which does nothing) which is useful for testing.

Building and Documentation
----------------------------

Details for how to build the robot and other information are in the ``docs`` folder in the `git repo <https://github.com/MomsFriendlyRobotCompany/quadruped/tree/master/docs>`_

Tools
---------

This directory contains several tools for the robot:

- get_leg_angles.py: prints out the joint angles for all 4 legs
- get_leg_info.py: prints out servo information for all 12 servos on the robot

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
