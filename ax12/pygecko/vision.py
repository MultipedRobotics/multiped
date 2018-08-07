#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import multiprocessing as mp
import time
import signal
# import imutils
from imutils.video import WebcamVideoStream
from the_collector.messages import Image

# from pygecko.transport import Pub, Sub
# from pygecko.transport import zmqTCP  #, GeckoCore
from pygecko.multiprocessing import geckopy
# from math import sin, cos, pi, sqrt
import numpy as np

try:
    import cv2
except ImportError:
    # this works the cpu! only for testing when opencv not installed
    from pygecko.test import cv2


def pcv(**kwargs):
    geckopy.init_node(**kwargs)
    rate = geckopy.Rate(10)

    p = geckopy.Publisher()

    camera = WebcamVideoStream(src=0).start()

    while not geckopy.is_shutdown():
        img = camera.read()

        if img is not None:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.resize(img, (640,480))
            msg = Image(img.shape, img.tobytes(), img.dtype)
            p.pub('images_color', msg)  # topic msg
            # p.pub(topic, {'a': 5})
            geckopy.log(img.shape)
        else:
            geckopy.log("*** couldn't read image ***")

        # sleep
        rate.sleep()

    camera.stop()
    print('cv bye ...')


if __name__ == "__main__":
    kw = {}

    pcv(kwargs=kw)
