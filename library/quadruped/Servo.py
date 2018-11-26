##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################


class Servo(object):
    """
    Servo hold the parameters of a servo, it doesn't talk to real servos. This
    class does the conversion between DH angles to real servo angles
    """

    def __init__(self, ID, offset=150):
        self.offset = offset
        # self.minAngle = minmax[0]  # DH space
        # self.maxAngle = minmax[1]  # DH space
        self.id = ID

    def DH2Servo(self, angle):
        """
        Sets the servo angle and clamps it between [limitMinAngle, limitMaxAngle].
        """
        sangle = angle+self.offset
        if sangle > 300 or sangle < 0:
            raise Exception('{} angle out of range DH[-150,150]: {:.1f}   Servo[0,300]: {:.1f} deg'.format(self.id, angle, sangle))
        return sangle
