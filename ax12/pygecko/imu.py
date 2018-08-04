#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import time
from pygecko.multiprocessing import GeckoPy
from messages import IMU, Vector

def bye():
    print('='*40)
    print(' lidar bye ...')
    print('='*40)


def imu(**kwargs):
    geckopy = GeckoPy(**kwargs)
    rate = geckopy.Rate(10)

    p = geckopy.Publisher()

    test = kwargs.get('test', True)

    while not geckopy.is_shutdown():
        if test:  # fake readings
            msg = IMU(
                Vector(1,2,3),
                Vector(1,2,3),
                Vector(1,2,3),
            )

            p.pub('imu', msg)

            msg = Vector(0,0,1)
            p.pub('unit_accel', msg)

        # sleep
        rate.sleep()


if __name__ == "__main__":
    kw = {'test': True}
    imu(kwargs=kw)
