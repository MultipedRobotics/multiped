# Bill of Materials

![system layout](pics/system_layout.png)

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
| 7.5V, 2.4A Buck Converter (D24V22F7)| [Pololu](https://www.pololu.com) | 1 | $10 | $10 | For powering the xl-320 |
| Dynamixel xl-320 smart servo        | [RobotShop](https://www.robotshop.com) | 12 | $22 | $264 |  |
| PS4 Controller                      | [Walmart](http://www.walmart.com) | 1 | $54 | $54 | |
| Micro SD (32 GB)                    | [Walmart](http://www.walmart.com) | 1 | $12 | $12 | Raspbian |
| 74LS241                             |                                   | 1 | $1 | $1 | Used to convert the RPi's RS232 into a RS485 port |
| Small signal MOSFET                 |                                  | 1 | $1  |    | Used for 3.3V to 5V conversion |
| 12V, 5A Wall Power Adaptor          | [Pololu](https://www.pololu.com) | 1 | $15 | $15 | So I don't have to always run off batteries |



---

<p align="center">
	<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
		<img alt="Creative Commons License"  src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" />
	</a>
	<br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
</p>

