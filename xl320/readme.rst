
.. image:: https://raw.githubusercontent.com/walchko/quadruped/master/pics/spiderbot_dev.JPG
	:target: https://github.com/MomsFriendlyRobotCompany/quadruped
	:width: 75%

XL-320 Quadruped
============================

My robot software.

* `YouTube <https://www.youtube.com/watch?v=kH2hlxUfCNg>`_
* `Vimeo <https://player.vimeo.com/video/194676675>`_


Documentation
-------------------

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

- Robot(data)
  - Takes a dict of setup values: {'serialPort': /dev/something, 'write': 'bulk'}
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
port which does nothing but is useful for testing.


Tools
---------

This directory contains several tools for the robot:

- get_leg_angles.py: prints out the joint angles for all 4 legs

.. code-block:: bash

	$ ./get_leg_angles.py /dev/tty.usbserial-AL034G2K
	Opened /dev/tty.usbserial-AL034G2K @ 1000000

	Servos: 1 - 12
	All angles are in degrees
	         Leg 1 |         Leg 2 |         Leg 3 |         Leg 4 |
	   ID | Angle  |   ID | Angle  |   ID | Angle  |   ID | Angle  |
	-----------------------------------------------------------------
	    1 | 149.56 |    4 | 149.56 |    7 | 149.56 |   10 | 149.56
	    2 | 239.88 |    5 | 271.55 |    8 | 269.79 |   11 | 270.38
	    3 |  99.41 |    6 | 100.29 |    9 | 100.00 |   12 |  99.41
	-----------------------------------------------------------------

- get_leg_info.py: prints out servo information for all 12 servos on the robot

.. code-block:: bash

	$ ./get_leg_info.py /dev/tty.usbserial-AL034G2K
	Opened /dev/tty.usbserial-AL034G2K @ 1000000

	Servos: 1 - 12
	--------------------------------------------------
	Servo: 1  		HW Error: 0
	Position [deg]: 149.6  Load:   0.0% CCW
	Voltage [V]  7.0     Temperature [F]:  80.6
	--------------------------------------------------
	Servo: 2  		HW Error: 0
	Position [deg]: 239.6  Load:   0.0% CCW
	Voltage [V]  7.2     Temperature [F]:  80.6
	--------------------------------------------------
	Servo: 3  		HW Error: 0
	Position [deg]:  99.4  Load:   0.0% CCW
	Voltage [V]  7.2     Temperature [F]:  82.4
	--------------------------------------------------
	Servo: 4  		HW Error: 0
	Position [deg]: 149.6  Load:   0.0% CCW
	Voltage [V]  7.3     Temperature [F]:  80.6
	--------------------------------------------------
	Servo: 5  		HW Error: 0
	Position [deg]: 271.6  Load:   0.0% CCW
	Voltage [V]  7.2     Temperature [F]:  80.6
	--------------------------------------------------
	Servo: 6  		HW Error: 0
	Position [deg]: 100.3  Load:   0.0% CCW
	Voltage [V]  7.4     Temperature [F]:  82.4
	--------------------------------------------------
	Servo: 7  		HW Error: 0
	Position [deg]: 149.6  Load:   0.0% CCW
	Voltage [V]  7.2     Temperature [F]:  80.6
	--------------------------------------------------
	Servo: 8  		HW Error: 0
	Position [deg]: 269.8  Load:   0.0% CCW
	Voltage [V]  7.1     Temperature [F]:  78.8
	--------------------------------------------------
	Servo: 9  		HW Error: 0
	Position [deg]:  99.4  Load:   0.8% CCW
	Voltage [V]  7.2     Temperature [F]:  82.4
	--------------------------------------------------
	Servo: 10  		HW Error: 0
	Position [deg]: 149.9  Load:   0.0% CCW
	Voltage [V]  7.1     Temperature [F]:  80.6
	--------------------------------------------------
	Servo: 11  		HW Error: 0
	Position [deg]: 270.1  Load:   0.0% CCW
	Voltage [V]  7.2     Temperature [F]:  80.6
	--------------------------------------------------
	Servo: 12  		HW Error: 0
	Position [deg]:  99.4  Load:   0.0% CCW
	Voltage [V]  7.1     Temperature [F]:  84.2
	--------------------------------------------------


Change Log
-------------

============ ======= ============================
2018-02-05   0.8.0   Code now supports both XL-320 and AX-12A servos
2017-12-25   0.5.0   Clean up and reorg, removed unnecessary libraries
2017-06-07   0.4.1   broke out into package and published to PyPi
2016-08-10   0.0.1   init
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
