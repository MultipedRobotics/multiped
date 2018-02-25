# Power System

## Voltage Converters

The main power is sized at 12V to provide xx W of power. Several highly
efficient buck converters are used to to translate the 12V into either
7.5V for the servos or 5V for the RPi.

### Servo Power

### RPi Power

## Power Budget

| Part          | Voltage In (V) | Current (mA) | Power (W) |
|---------------|----------------|--------------|-----------|
| RPi           | 5              | 2000         | 10        |
| Pi Camera     | 3.3            | 250          | 0.825     |
| 5V Converter  | 5              | 5000         | 2.5 @ 90% |
| 7.2V Converter| 7.2            | 5000         | 3.6 @ 90% |
| xl-320 (x12)  | 7.2            | 1000         | 7.2 (86.4)|
| IMU           | 3.3            | 2.7 + 1      | 0.007     |
| Audio Amp     | 5              | 600          | 3         |

**Note:** The currents are worst cases. The servos and RPi are not expected to 
continously pull this much current.

---

<p align="center">
	<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
		<img alt="Creative Commons License"  src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" />
	</a>
	<br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
