#!/usr/bin/env python
from __future__ import print_function
from __future__ import division
import numpy as np
import time
import cv2

# This is a simple pink raquetball finder algorithm using upper/lower HSV
# bounds to detect the ball. It works ok.


def find_ball(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    ballUpper = (330/2, .9*255, 1*250)
    ballLower = (290/2,  .6*255, .2*255)
    detect = cv2.inRange(hsv, ballLower, ballUpper)
    erode = cv2.erode(detect, None, iterations=5)
    dilate = cv2.dilate(erode, None, iterations=8)
    # cv2.imwrite("ball.jpg", dilate)

    cv2.imshow('original', img)
    cv2.imshow('dilate', dilate)
    cnts = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if cnts:
        print('Found {} objects'.format(len(cnts)))
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        x, y, radius = int(x), int(y), int(radius)
        print('Circle center: ({}, {})   radius: {} pixels'.format(x, y, radius))
    else:
        print("None")


# def drive(x, y, radius):
#     if(x>350):
#         bot.turn_angle(-5,200)
#     elif(x<290):
#         bot.turn_angle(5,200)
#     if(radius<20):
#         bot.drive_distance(.1,200)
#     elif(radius>30):
#         bot.drive_distance(.1,-200)
#     bot.drive_stop()


if __name__ == "__main__":
    cam = cv2.VideoCapture(0)
    while True:
        ok, img = cam.read()
        if ok:
            find_ball(img)

        key = cv2.waitKey(100)
        if key & 0xff == ord('q'):
            break
        if key &  0xff == ord('s'):
            cv2.imwrite('ball.png', img)
            time.sleep(1)

    cam.release()
