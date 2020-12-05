from math import sin, cos, pi
import numpy as np
import time

class Vector:
    __data = None

    def __init__(self, x=0,y=0,z=0):
        self.__data = [x,y,z]

    def __index__(self, i):
        return self.__data[i]

    @property
    def x(self):
        return self.__data[0]
    @x.setter
    def x(self, x):
        self.__data[0] = x

    @property
    def y(self):
        return self.__data[1]
    @y.setter
    def y(self, y):
        self.__data[1] = y

    @property
    def z(self):
        return self.__data[2]
    @z.setter
    def z(self, z):
        self.__data[2] = z

class Foot:
    position = None
    orientation = 0 # yaw only
    cycle = 0

    def __init__(self, x=0, y=0, z=0, theta=0, cycle=0):
        self.position = Vector(x,y,z)
        self.orientation = theta
        self.cycle = cycle

class Twist:
    linear = Vector()
    angular = Vector()

class Pose2D:
    x = 0
    y = 0
    theta = 0




class Gait:
    def __init__(self):
        self.cycle_period = 25

        # tripod
        self.gait_factor = 1.0
        # self.cycle_leg_number = [1,0,1,0,1,0] # Leg gait order (grouping) ['RR', 'RM', 'RF', 'LR', 'LM', 'LF']
        self.last_time = time.monotonic()
        self.cycle_length = ?? # config
        self.leg_lift_height = 50 # config

        self.feet = [
            Foot(cycle=1),
            Foot(cycle=0),
            Foot(cycle=1),
            Foot(cycle=0),
            Foot(cycle=1),
            Foot(cycle=0)
        ]

        self.lpf = Pose2D()

    def cyclePeriod(self, base, gait_vel):
        period_height = sin(self.cycle_period*pi/self.cycle_length)

        current_time = time.monotonic()
        dt = current_time - self.last_time
        self.last_time = current_time

        gait_vel.linear.x = pi*base.x / cycle_length * period_height * (1/dt)
        gait_vel.linear.y = -pi*base.y / cycle_length * period_height * (1/dt)
        gait_vel.angular.z = pi*base.theta * period_height * (1/dt)

        for i, foot in enumerate(self.feet):
            if foot.cycle == 0:
                period_distance = cos( self.cycle_period * pi / self.cycle_length)
                foot.position.x = base.x * period_distance
                foot.position.y = base.y * period_distance
                foot.position.z = leg_lift_height * period_height
                foot.orientation = base.theta * period_distance
            elif foot.cycle == 1:
                period_distance = cos( self.cycle_period * pi / self.cycle_length)
                foot.position.x = -base.x * period_distance
                foot.position.y = -base.y * period_distance
                foot.position.z = 0
                foot.orientation = -base.theta * period_distance

    def gaitCycle(self, cmd_vel, gait_vel):
        base = Pose2D()
        base.x = cmd_vel.linear.x / pi * cycle_length
        base.y = cmd_vel.linear.y / pi * cycle_length
        base.theta = cmd_vel.angular.z / pi * cycle_length

        # Low pass filter on the values to avoid jerky movements due to rapid value changes
        smooth_base = self.lpf
        smooth_base.x = base.x * 0.05 + ( smooth_base.x * ( 1.0 - 0.05 ) );
        smooth_base.y = base.y * 0.05 + ( smooth_base.y * ( 1.0 - 0.05 ) );
        smooth_base.theta = base.theta * 0.05 + ( smooth_base.theta * ( 1.0 - 0.05 ) );

        if abs(self.lpf.x) > 0.001 or abs(self.lpf.y) > 0.001 or abs(self.lpf.theta) > 0.0043:
            self.is_travelling = True
        else:
            self.is_travelling = False

            # check if in non-rest position

        if self.is_travelling is True or in_cycle is True:
            self.cyclePeriod(self.lpf, gait_vel)
            self.cycle_period += 1
        else:
            self.cycle_period = 0

        if self.cycle_period == self.cycle_length:
            self.cycle_period = 0

            # switch sequence on the foot cycle
            for foot in self.feet:
                if foot.cycle == 0:
                    foot.cycle = 1
                else:
                    foot.cycle = 0

























##
