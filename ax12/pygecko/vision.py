#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import multiprocessing as mp
import time
import signal
# import imutils
from imutils.video import WebcamVideoStream
from pygecko.messages import Image

# from pygecko.transport import Pub, Sub
# from pygecko.transport import zmqTCP  #, GeckoCore
from pygecko.multiprocessing import geckopy
# from math import sin, cos, pi, sqrt
import numpy as np
from collections import namedtuple

try:
    import cv2
except ImportError:
    # this works the cpu! only for testing when opencv not installed
    from pygecko.test import cv2


Target = namedtuple('Target', 'center radius')


def find_ball(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    ballUpper = (330/2, .9*255, 1*250)
    ballLower = (290/2,  .6*255, .2*255)
    detect = cv2.inRange(hsv, ballLower, ballUpper)
    erode = cv2.erode(detect, None, iterations=5)
    dilate = cv2.dilate(erode, None, iterations=8)
    # cv2.imwrite("ball.jpg", dilate)

    # cv2.imshow('original', img)
    # cv2.imshow('dilate', dilate)
    cnts = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    ret = None
    if cnts:
        print('Found {} objects'.format(len(cnts)))
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        x, y, radius = int(x), int(y), int(radius)
        ret = Target((x,y), (radius))
        # print('Circle center: ({}, {})   radius: {} pixels'.format(x, y, radius))
    # else:
    #     print("None")
    return ret


def pcv(**kwargs):
    geckopy.init_node(**kwargs)
    rate = geckopy.Rate(10)

    p = geckopy.Publisher()

    camera = WebcamVideoStream(src=0).start()

    while not geckopy.is_shutdown():
        img = camera.read()

        if img is not None:
            # geckopy.log(img.shape)
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.resize(img, (640,480))
            msg = find_ball(img)
            # msg = Image(img.shape, img.tobytes(), img.dtype)
            if msg:
                # p.pub('images_color', msg)  # topic msg
                p.pub('target', msg)
                geckopy.log(msg)
            # p.pub(topic, {'a': 5})
            # geckopy.log(img.shape)
        else:
            geckopy.log("*** couldn't read image ***")

        # sleep
        rate.sleep()

    camera.stop()
    print('cv bye ...')


if __name__ == "__main__":
    kw = {}

    pcv(kwargs=kw)
