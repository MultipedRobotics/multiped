# Bill of Materials

## Raspberry Pi

I am currently using a 1.2 GHz quad core [RPi 3](https://www.adafruit.com/products/3055)
(ARMv8) as the main board running the lite version of Raspbian. It has on-board:

* 802.11n Wifi
* Bluetooth 4.1 BLE

![](pics/sider_pinout.jpg)

## Pi Camera

[PiCamera](https://www.adafruit.com/products/3099) is used to stream images.

### 3D Models

The 3d printer models (stl format) come from the following sources:

* [Legs](https://github.com/mogillc/nico) which are the coxa, femur, and tibia
* Misc brackets I made using [OpenScad](http://www.openscad.org/)
* [Rivets](http://www.robotis.us/rivet-set-rs-10/) to put the frame together with

# Cost

Here is a parts list of **key components** that I am using. I am not listing
wires, bread boards, cables, etc. Also note, I have rounded up the costs
(i.e., $4.95 => $5). Also, lot of the body is 3d printed, the costs for that are
not shown here.

| Part | Source | Number | Item Cost | Sum | Notes |
| ---  | ---    | ---    | ---       | --- | ---   |
| RPi v3                              | [Adafruit](https://www.adafruit.com) | 1 | $40 | $40 | Main board, has wifi and bluetooth already |
| Pi Camera                           | [Adafruit](https://www.adafruit.com) | 1 | $30 | $30 | 8 Mpixel |
| 5V, 5A Buck Converter (D24V22F5)    | [Pololu](https://www.pololu.com) | 1 | $10 | $10 | For powering the RPi |
| Matek 7.2V, 5A buck converter       | [Amazon](https://www.amazon.com) | 1 | $15 | $15 | For powering the xl-320 |
| Dynamixel xl-320 smart servo        | [RobotShop](https://www.robotshop.com) | 12 | $22 | $264 |  |
| Rivets for xl-320                   | [Robotus.us](http://www.robotis.us/rivet-set-rs-10/) | 1 | $6 | $6 | There are about 250 in a bag|
| PS4 Controller                      | [Walmart](http://www.walmart.com) | 1 | $54 | $54 | |
| Micro SD (16 GB)                    | [Walmart](http://www.walmart.com) | 1 | $7  | $7  | Raspbian |
| 74LS126                             |                                   | 1 | $1 | $1 | Used talk with the xl-320 |
| MCP3208 12b 8 ch SPI ADC            |                                   | 1 | $4 | $4 | | 
| NXP IMU                             | [Adafruit](https://www.adafruit.com/product/3463) | 1 | $14 | $14 | |
| USB-serial port 5V logic            | [Sparkfun](https://www.sparkfun.com/products/9716) | 1 | $14 | $14 | Make sure it is a real FTDI with 5V logic |
| 12V, 5A Wall Power Adaptor          | [Pololu](https://www.pololu.com) | 1 | $15 | $15 | So I don't have to always run off batteries |



---

<p align="center">
	<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
		<img alt="Creative Commons License"  src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" />
	</a>
	<br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
</p>

