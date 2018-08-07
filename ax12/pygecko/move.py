#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import time

from pygecko.multiprocessing import geckopy
import itertools


def movement(**kwargs):
    geckopy.init_node(**kwargs)
    rate = geckopy.Rate(1)

    path = [
        (1.0,0,0,),
        (1.0,0,0,),
        (1.0,0,0,),
        (1.0,0,0,),
        (1.0,0,0,),
        (1.0,0,0,),
    ]

    p = geckopy.Publisher()
    i = 0
    cmd = itertools.cycle(path)
    while not geckopy.is_shutdown():
        msg = next(cmd)
        p.pub('cmd', msg)  # topic msg
        geckopy.log(msg)

        # geckopy.log('[{}] published: {}'.format(i, msg))
        # i = (i + 1) % len(path)
        rate.sleep()
    print('pub bye ...')


if __name__ == "__main__":
    kw = {}
    movement(kwargs=kw)
