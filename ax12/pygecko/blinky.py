#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
from __future__ import print_function
import time
from led_matrix import LEDDisplay
from pygecko.multiprocessing import geckopy


def got_msg(t, m):
    # want to do something if message arrives
    pass


def matrix(**kwargs):
    geckopy.init_node(**kwargs)
    rate = geckopy.Rate(10)
    test = kwargs.get('test', False)

    s = geckopy.Subscriber(['led'], got_msg)

    while not geckopy.is_shutdown():
        # if s has message, call function
        # else update led

        rate.sleep()


if __name__ == "__main__":
    kw = {'test': True}
    matrix(kwargs=kw)
