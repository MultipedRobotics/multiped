from math import cos, sin, sqrt, pi, atan2


# debug = False


def rot_z_tuple(t, c):
    """
    t - theta [radians]
    c - [x,y,z]
    return - (x,y,z) tuple rotated about z-axis
    """
    ans = (
        c[0]*cos(t)-c[1]*sin(t),
        c[0]*sin(t)+c[1]*cos(t),
        c[2]
    )

    return ans


# make a static method in Gait? Nothing else uses it
def rot_z(t, c):
    """
    t - theta [radians]
    c - [x,y,z]
    return - [x,y,z] numpy array rotated about z-axis
    """
    ans = [
        c[0]*cos(t)-c[1]*sin(t),
        c[0]*sin(t)+c[1]*cos(t),
        c[2]
    ]

    return ans


class Gait(object):
    """
    Base class for gaits. Gait only plan all foot locations for 1 complete cycle
    of the gait.

    Like to add center of mass (CM) compensation, so we know the CM is always
    inside the stability triangle.

    Gait knows:
    - how many legs
    - leg stride (neutral position)
    """
    # these are the offsets of each leg
    # legOffset = [0, 3, 3, 0]
    # frame rotations for each leg
    # frame = [pi/4, -pi/4, -3*pi/4, 3*pi/4]  # frame 0, 1, 2, 3
    # frame = [0, -pi/4, -3*pi/4, 3*pi/4]  # frame 0, 1, 2, 3
    # moveFoot = None
    rest = None
    # scale = 50.0

    def __init__(self, rest):
        # the resting or idle position/orientation of a leg
        self.rest = rest # (x,y,z,)

    def command(self, cmd):
        """
        Send a command to the quadruped
        cmd: [x, y, rotation about z-axis], the x,y is a unit vector and
        rotation is in radians
        """
        x, y, rz = cmd
        d = sqrt(x**2+y**2)

        # handle no movement command ... do else where?
        if d <= 0.1 and abs(rz) < 0.1:
            x = y = 0.0
            rz = 0.0
            return None
        # commands should be unit length, oneCyle scales it
        elif 0.1 < d:
            x /= d
            y /= d
        # else:
        #     return None

        angle_limit = pi/2
        if rz > angle_limit:
            rz = angle_limit
        elif rz < -angle_limit:
            rz = -angle_limit

        return self.oneCycle(x, y, rz)

    def oneCycle(self, x, y, rz):
        raise NotImplementedError('*** Gait: wrong function, this is base class! ***')



#########################################################################


class Discrete(Gait):
    """
    Discrete 12 step gait
    """
    steps = 0

    def __init__(self, rest):
        """
        height: added to z
        rest: the neutral foot position
        """
        Gait.__init__(self, rest)

        self.rest = rest
        zd = 0
        zu = -self.rest[2]
        x = self.rest[0]

        # min/max = 0.75 works for straight
        # min/max = [.25,.5] for 45deg
        ratio = (0.75, 0.75,)  # use this for below, min/max???
        ratio = (0.25, 0.5,)  # works for all angles
        self.points = {
            'A': (-x*.75, 0, zd,),  # A - closest point
            'B': (x*.75, 0, zd,),   # B - farthest point
            'N': (0, 0, zd,),     # N - netural point
            'a': (-x*.75, 0, zu),   # A lifted up
            'b': (x*.75, 0, zu,)    # B lifted up
        }

        # A,a',b',B,N,n,n,N,n,n,N,A,a,a,a
        # 0/3
        self.steps = [
            self.points['A'],self.points['a'],self.points['b'],
            self.points['B'],self.points['N'],self.points['N'],self.points['N'],
            self.points['N'],self.points['N'],self.points['N'],
            self.points['N'],self.points['A'],self.points['A'],self.points['A'],self.points['A']
        ]
        # 1/2
        self.steps2 = [
            self.points['N'],self.points['N'],self.points['N'],
            self.points['N'],self.points['A'],self.points['A'],self.points['A'],
            self.points['A'],self.points['a'],self.points['b'],
            self.points['B'],self.points['N'],self.points['N'],self.points['N'],self.points['N']
        ]

        self.legOffset = [0, 0, 14, 14]
        self.frame = [pi/4, -pi/4, -3*pi/4, 3*pi/4]  # frame 0, 1, 2, 3

    def eachLeg(self, step, index, cmd, legNum):
        """
        interpolates the foot position of each leg
        cmd:
            linear (mm)
            angle (rads)
        """
        x,y,rz = cmd
        mag = abs(x**2 + y**2)
        angle = atan2(y,x)

        # this gets a delta from neutral
        if legNum in [0,3]:
            cmd = self.steps[index]
        else:
            cmd = self.steps2[index]

        # print(cmd)

        rcmd = rot_z_tuple(self.frame[legNum]+angle, cmd)
        rest = self.rest
        newpos = [0, 0, 0]
        if legNum in [2,3]:
            rcmd = (-rcmd[0], -rcmd[1], rcmd[2],)
        newpos[0] = rcmd[0] + rest[0]
        newpos[1] = rcmd[1] + rest[1]
        newpos[2] = rcmd[2] + rest[2]
        # else:
        #     newpos = self.steps2[index]

        print('  [{}](x,y,z): {:.2f} {:.2f} {:.2f}'.format(legNum, newpos[0], newpos[1], newpos[2]))
        return newpos

    def oneCycle(self, x, y, rz):
        """
        direction of travel x, y (2D plane) or rotation about z-axis
        Returns 1 complete cycle for all 4 feet (x,y,z)
        """

        # check if x, y, rz is same as last time commanded, if so, return
        # the last cycle response, else, calculate a new response
        # ???

        # scale = self.scale
        # cmd = (scale*x, scale*y, rz)
        ret = {
            0: [],
            1: [],
            2: [],
            3: []
        }  # 4 leg foot positions for the entire 12 count cycle is returned

        num = len(self.steps)
        for i in range(num):
            print("Step[{}]-----------".format(i))
            for legNum in [0, 1, 2, 3]:
                # rcmd = cmd
                # rcmd = rot_z_tuple(self.frame[legNum], cmd)
                if legNum in [0,1]:
                    index = (i + self.legOffset[legNum]) % num
                else:
                    index = (num - (i - self.legOffset[legNum])) % num
                # print("  0: {}".format(index))

                pos = self.eachLeg(i,index, (x,y,rz), legNum)  # move each leg appropriately
                # print('Foot[{}]: {:.2f} {:.2f} {:.2f}'.format(legNum, *(pos)))

                ret[legNum].append(pos)

        # if debug:
        #     print("=[Gait.py]===============================")
        #     for legNum in [0, 1, 2, 3]:
        #         print('Leg[{}]---------'.format(legNum))
        #         for i, pt in enumerate(ret[legNum]):
        #             print('  {:2}: {:7.2f} {:7.2f} {:7.2f}'.format(i, *pt))

        # update leg positions
        # self.current_position = ['A','N','N','A']

        return ret
