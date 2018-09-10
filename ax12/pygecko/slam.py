#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import time
import platform
from sslam import RMHC_SLAM
from sslam import LDS01_Model
# from pydar import LDS01
# from pltslamshow import SlamShow

from pygecko.multiprocessing import geckopy
from pygecko import Lidar

# def bye():
#     print('='*40)
#     print(' lidar bye ...')
#     print('='*40)


# def range_filter(scan, range, min=10):
#     """
#     scan: array of lidar data in the format (deg, range[mm])
#     range: distance threshold to report if less than range in mm
#     return: an array of obstacles
#     """
#     ob = []
#     for d, r in scan:
#         if min < r <= range:
#             ob.append((d,r,))
#
#     return ob

def slam_publisher(**kwargs):
    geckopy.init_node(**kwargs)
    rate = geckopy.Rate(10)

    geckopy.log(kwargs)

    
    p = geckopy.Publisher()

    test = kwargs.get('test', False)
    # MAP_SIZE_PIXELS         = 500
    # MAP_SIZE_METERS         = 10

    if platform.system() == 'Linux':
        port = '/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0'
    else:
        port = "/dev/tty.SLAB_USBtoUART"

    # Connect to Lidar unit
    lidar = LDS01()
    lidar.open(port)
    lidar.run(True)

    # Create an RMHC SLAM object with a laser model and optional robot model
    # slam = RMHC_SLAM(LDS01_Model(), MAP_SIZE_PIXELS, MAP_SIZE_METERS)

    # Set up a SLAM display
    # display = SlamShow(MAP_SIZE_PIXELS, MAP_SIZE_METERS*1000/MAP_SIZE_PIXELS, 'SLAM')

    # Initialize empty map
    # mapbytes = bytearray(MAP_SIZE_PIXELS * MAP_SIZE_PIXELS)

    while not geckopy.is_shutdown():
        # Update SLAM with current Lidar scan
        pts = lidar.read()
        # need to reverse the order for it to plot correctly
        pts = list(reversed(pts))

        # kludge until i fix the driver
        scan = []
        for i, p in enumerate(pts):
            scan.append((i,p,))

        msg = Lidar(scan)

        if test:
            print("[LIDAR]=================")
            print("  points: {}".format(len(msg.scan)))
            print("  pt[0]: {}".format(msg.scan[0]))
            print("  timestamp: {}".format(msg.timestamp))

            obs = range_filter(scan, 200)
            print("[Obstacles]=============")
            print("  number: {}".format(len(obs)))
            print("  obs: {}".format(obs))
        else:
            p.pub('scan', msg)

        # slam.update(pts)

        # Get current robot position
        # x, y, theta = slam.getpos()

        # Get current map bytes as grayscale
        # slam.getmap(mapbytes)

        # display.displayMap(mapbytes)
        # display.setPose(x, y, theta)
        # display.refresh()

        # p.pub('avoid', msg)
        # geckopy.log(msg)

        # sleep
        rate.sleep()

    # all done
    lidar.close()


if __name__ == "__main__":
    kw = {'test': True}
    lidar_publisher(**kw)
