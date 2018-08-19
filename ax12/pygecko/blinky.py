#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# sudo i2cdetect -y 1
from __future__ import print_function
import time
from led_matrix import LEDDisplay
from pygecko.multiprocessing import geckopy


def got_msg(t, m):
    # want to do something if message arrives
    pass


def matrix(**kwargs):
    geckopy.init_node(**kwargs)
    rate = geckopy.Rate(1)
    test = kwargs.get('test', False)
    matrix = LEDDisplay()

    s = geckopy.Subscriber(['led'], got_msg)
    i = 0

    while not geckopy.is_shutdown():
        # if s has message, call function
        # else update led
        geckopy.log('x')

        # matrix.setRandom()
        matrix.update()
        # matrix.set(1,1,127)
        # matrix.clear()
        # matrix.display.set_pixel(i//8,i%8, 1)
        # matrix.write()
        # i = (i+1)%64

        rate.sleep()


if __name__ == "__main__":
    kw = {'test': True}
    matrix(kwargs=kw)
