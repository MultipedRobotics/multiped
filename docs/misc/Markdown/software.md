# Software

Go to the install_software folder and follow the directions.

## pyXL320

This software requires [pyxl320](https://pypi.python.org/pypi/pyxl320) to work
with the smart servos. You can install it with:

	pip install pyxl320

Since all of the leg servos are on the same RS845 bus, you will need to use
`set_id` to assign an *id* number to each servo **BEFORE** you hook them all
together. To see how to use it, type:

	set_id --help

## Tests

`nose` is used for unit tests ... just run `nosetests -vs *.py`.

## Quadruped Driver

If you look in the `quadruped` folder, it contains the low level driver:

* SimpleQuadruped.py - basic wrapper around leg and gait algorithms
* Leg.py - forward/reverse kinematics and contains an array of servos for each joint
* Gait.py - syncronization of how the 4 legs walk and is basically a planner
* Servo.py - talks to the XL-320 smart servos

---

<p align="center">
	<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
		<img alt="Creative Commons License"  src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" />
	</a>
	<br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
</p>
