from __future__ import division
from __future__ import print_function
import os
# import numpy as np
# import random
from time import sleep

# try:
#     from Adafruit_LED_Backpack.Matrix8x8 import Matrix8x8
#     from Adafruit_LED_Backpack.BicolorMatrix8x8 import BicolorMatrix8x8
#     from Adafruit_LED_Backpack.BicolorMatrix8x8 import RED, GREEN
# except ImportError:
#     print('<<< using fake led_matrix >>>')
#     # Fake i2c class for testing on non-raspberry pi hardware
#     class fake_i2c(object):
#         buffer = []
#         def __init__(self, **kwargs): pass
#         def set_led(self, a, b, c): pass
#         def set_pixel(self, a, b, c): pass
#         def clear(self): pass
#         def writeList(self, a, b): pass
#         def begin(self): pass
#         def start(self): pass
#
#     class Matrix8x8(fake_i2c):
#         _device = fake_i2c()
#         def __init__(self, **kwargs): pass
#
#     class BicolorMatrix8x8(fake_i2c):
#         def __init__(self, **kwargs): pass
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# from __future__ import division


# Constants
DEFAULT_ADDRESS             = 0x70
HT16K33_BLINK_CMD           = 0x80
HT16K33_BLINK_DISPLAYON     = 0x01
HT16K33_BLINK_OFF           = 0x00
HT16K33_BLINK_2HZ           = 0x02
HT16K33_BLINK_1HZ           = 0x04
HT16K33_BLINK_HALFHZ        = 0x06
HT16K33_SYSTEM_SETUP        = 0x20
HT16K33_OSCILLATOR          = 0x01
HT16K33_CMD_BRIGHTNESS      = 0xE0


class HT16K33(object):
    """Driver for interfacing with a Holtek HT16K33 16x8 LED driver."""

    def __init__(self, address=DEFAULT_ADDRESS, i2c=None, **kwargs):
        """Create an HT16K33 driver for device on the specified I2C address
        (defaults to 0x70) and I2C bus (defaults to platform specific bus).
        """
        if i2c is None:
            import Adafruit_GPIO.I2C as I2C
            i2c = I2C
        self._device = i2c.get_i2c_device(address, **kwargs)
        # self.buffer = bytearray([0]*16)
        self.clear()

    def begin(self):
        """Initialize driver with LEDs enabled and all turned off."""
        # Turn on the oscillator.
        self._device.writeList(HT16K33_SYSTEM_SETUP | HT16K33_OSCILLATOR, [])
        # Turn display on with no blinking.
        self.set_blink(HT16K33_BLINK_OFF)
        # Set display to full brightness.
        self.set_brightness(15)

    def set_blink(self, frequency):
        """Blink display at specified frequency.  Note that frequency must be a
        value allowed by the HT16K33, specifically one of: HT16K33_BLINK_OFF,
        HT16K33_BLINK_2HZ, HT16K33_BLINK_1HZ, or HT16K33_BLINK_HALFHZ.
        """
        if frequency not in [HT16K33_BLINK_OFF, HT16K33_BLINK_2HZ,
                             HT16K33_BLINK_1HZ, HT16K33_BLINK_HALFHZ]:
            raise ValueError('Frequency must be one of HT16K33_BLINK_OFF, HT16K33_BLINK_2HZ, HT16K33_BLINK_1HZ, or HT16K33_BLINK_HALFHZ.')
        self._device.writeList(HT16K33_BLINK_CMD | HT16K33_BLINK_DISPLAYON | frequency, [])

    def set_brightness(self, brightness):
        """Set brightness of entire display to specified value (16 levels, from
        0 to 15).
        """
        if brightness < 0 or brightness > 15:
            raise ValueError('Brightness must be a value of 0 to 15.')
        self._device.writeList(HT16K33_CMD_BRIGHTNESS | brightness, [])

    def set_led(self, led, value):
        """Sets specified LED (value of 0 to 127) to the specified value, 0/False
        for off and 1 (or any True/non-zero value) for on.
        """
        if led < 0 or led > 127:
            raise ValueError('LED must be value of 0 to 127.')
        # Calculate position in byte buffer and bit offset of desired LED.
        pos = led // 8
        offset = led % 8
        if not value:
            # Turn off the specified LED (set bit to zero).
            self.buffer[pos] &= ~(1 << offset)
        else:
            # Turn on the speciried LED (set bit to one).
            self.buffer[pos] |= (1 << offset)

    # def write_display(self):
    #     """Write display buffer to display hardware."""
    #     for i, value in enumerate(self.buffer):
    #         self._device.write8(i, value)
    def write(self):
        self._device.writeList(0, self.buffer)

    def clearBuffer(self):
        """Clear contents of display buffer."""
        self.buffer = bytearray([0]*16)

    def clear(self):
        self.clearBuffer()
        self.write()


class Matrix8x8(HT16K33):
    """Single color 8x8 matrix LED backpack display."""

    def __init__(self, **kwargs):
        """Initialize display.  All arguments will be passed to the HT16K33 class
        initializer, including optional I2C address and bus number parameters.
        """
        # super(Matrix8x8, self).__init__(**kwargs)
        HT16K33.__init__(self,**kwargs)

    def set_pixel(self, x, y, value):
        """Set pixel at position x, y to the given value.  X and Y should be values
        of 0 to 7.  Value should be 0 for off and non-zero for on.
        """
        if x < 0 or x > 7 or y < 0 or y > 7:
            # Ignore out of bounds pixels.
            return
        self.set_led(y * 16 + ((x + 7) % 8), value)


class LEDDisplay(object):
    """
    This class handles the LED matrix
    OFF    = 0
    ON     = 1
    """

    def __init__(self, i2c_addr=0x70):
        # self.delay = delay
        # print(i2c_addr,led_type)
        self.im = []
        self.blocks = []
        self.blocks.append(bytearray([0x0]*8) + bytearray([0x87]*8))
        self.blocks.append(bytearray([0x0]*8) + bytearray([0x78]*8))
        self.blocks.append(bytearray([0x78]*8) + bytearray([0x0]*8))
        self.blocks.append(bytearray([0x87]*8) + bytearray([0x0]*8))
        self.block_num = 0

        self.display = Matrix8x8(address=i2c_addr)
        # self.set_brightness(10)

        # for i in range(10):
        #     self.im.append(bytearray(os.urandom(16)))

        self.display.begin()
        self.display.clear()

        # dim leds 0 - 15
        # self.display._device.writeList(0xE0 | 3, [])
        self.display.set_brightness(3)

        # self.next = 0

    def __del__(self):
        self.clear()
        sleep(0.005)

    def clear(self):
        self.display.clear()
    #     self.display._device.writeList(0, self.display.buffer)

    def set(self, x, y, val=1):
        # self.display.set_pixel(x, y, color)
        self.display.set_led(0,val)
        self.display.write()

    def displaySet(self, im):
        self.display.buffer = im
        self.display.write()

    def setSolid(self):
        self.display.buffer = bytearray([0xff]*16)
        self.display.write()

    def setRandom(self):
        self.display.buffer = bytearray(os.urandom(16))
        self.display.write()

    def update(self):
        # self.display.clear()
        self.display.buffer = self.blocks[self.block_num]
        self.display.write()
        self.block_num = (self.block_num + 1) % 4

    def write(self):
        self.display.write()
    #     self.display._device.writeList(0, self.display.buffer)
