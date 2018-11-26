import numpy as np
from matplotlib import pyplot as plt
from math import sin, cos, pi

def rplot(t1, t2, t3, t4, degrees=True):
    """Given the 4 joint angles (in rads), plot the arm in the x-y and w-z planes

    x = (d2 + l1*cos(t2) + l2*cos(t2 + t3) + l3*cos(t2 + t3 + t4))*cos(t1)
    y = (d2 + l1*cos(t2) + l2*cos(t2 + t3) + l3*cos(t2 + t3 + t4))*sin(t1)
    z = l1*sin(t2) + l2*sin(t2 + t3) + l3*sin(t2 + t3 + t4)
    """
    l1 = 52
    l2 = 89
    l3 = 90
    l4 = 95

    ptsx = [0]
    ptsy = [0]

    print(">> rplot angles")
    print(" 0: {:1f} 1: {:1f} 2: {:1f} 3: {:1f}".format(t1,t2,t3,t4))

    # handle offsets
    # t1 += 0
    # t2 += 27
    # t3 += (71-27)
    # t4 += 17

    if degrees:
        t1 *= pi/180
        t2 *= pi/180
        t3 *= pi/180
        t4 *= pi/180


    # our definition is reverse or these joints
    # link 1
    x0 = l1
    y0 = 0
    ptsx.append(x0)
    ptsy.append(y0)

    # link 2
    x1 = x0 + l2*cos(t2)
    y1 = y0 + l2*sin(t2)
    ptsx.append(x1)
    ptsy.append(y1)

    # link 3
    x2 = x1 + l3*cos(t2 + t3)
    y2 = y1 + l3*sin(t2 + t3)
    ptsx.append(x2)
    ptsy.append(y2)

    # link 4
    x3 = x2 + l4*cos(t2 + t3 + t4)
    y3 = y2 + l4*sin(t2 + t3 + t4)
    ptsx.append(x3)
    ptsy.append(y3)

    plt.ion()
    plt.subplot(1,2,1,projection='polar')
    plt.plot([0, t1], [0, 1.0])
    plt.grid(True)
    plt.title('Azimuth Angle (x-y plane)\n')

    plt.subplot(1,2,2)
    plt.plot(ptsx, ptsy, 'b-', marker='o')
    plt.axis('equal')
    plt.grid(True)
    plt.title('w-z Plane')
    # plt.show()
    plt.pause(1)


def rplot2(angles, pause=1, degrees=True):
    """Given the 4 joint angles (in rads), plot the arm in the x-y and w-z planes

    x = (d2 + l1*cos(t2) + l2*cos(t2 + t3) + l3*cos(t2 + t3 + t4))*cos(t1)
    y = (d2 + l1*cos(t2) + l2*cos(t2 + t3) + l3*cos(t2 + t3 + t4))*sin(t1)
    z = l1*sin(t2) + l2*sin(t2 + t3) + l3*sin(t2 + t3 + t4)
    """
    l1 = 52
    l2 = 89
    l3 = 90
    l4 = 95

    # plt.subplot(1,2,1,projection='polar')
    # plt.ion()

    for t1,t2,t3,t4,speed in angles:

        ptsx = [0]
        ptsy = [0]

        print(">> rplot angles")
        print(" 0: {:1f} 1: {:1f} 2: {:1f} 3: {:1f}".format(t1,t2,t3,t4))

        # handle offsets
        # t1 += 0
        # t2 += 27
        # t3 += (71-27)
        # t4 += 17

        if degrees:
            t1 *= pi/180
            t2 *= pi/180
            t3 *= pi/180
            t4 *= pi/180

        # our definition is reverse or these joints
        # link 1
        x0 = l1
        y0 = 0
        ptsx.append(x0)
        ptsy.append(y0)

        # link 2
        x1 = x0 + l2*cos(t2)
        y1 = y0 + l2*sin(t2)
        ptsx.append(x1)
        ptsy.append(y1)

        # link 3
        x2 = x1 + l3*cos(t2 + t3)
        y2 = y1 + l3*sin(t2 + t3)
        ptsx.append(x2)
        ptsy.append(y2)

        # link 4
        x3 = x2 + l4*cos(t2 + t3 + t4)
        y3 = y2 + l4*sin(t2 + t3 + t4)
        ptsx.append(x3)
        ptsy.append(y3)

        plt.subplot(1,2,1,projection='polar')
        plt.plot([0, t1], [0, 1.0])
        plt.grid(True)
        plt.title('Azimuth Angle (x-y plane)\n')

        plt.subplot(1,2,2)
        plt.plot(ptsx, ptsy, 'b-', marker='o')
        plt.axis('equal')
        plt.grid(True)
        plt.title('w-z Plane')
        # plt.show()
        plt.pause(pause)

    plt.show()


def plot_body_frame(pts, pause=1):
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

#     import pylab
#     pylab.rcParams['figure.figsize'] = (15.0, 15.0)

    # plot things in global body frame
    dy = 135/2
    dx = 95/2
    body = [(dx,-dy), (dx,dy),(-dx,dy),(-dx,-dy)] # CCW
#     frame = [pi/4, -pi/4, -3*pi/4, 3*pi/4]
    frame = [-pi/4, pi/4, 3*pi/4, -3*pi/4]
    feet = {
        0: [],
        1: [],
        2: [],
        3: []
    }

    for leg in range(4):
        for pos in pts[leg]:
            rpt = rot_z(frame[leg], pos)
            feet[leg].append((body[leg][0] + rpt[0], body[leg][1] + rpt[1], rpt[2]))

    for step in range(len(feet[0])):
        # ax = plt.subplot(4,3,step+1)
        ax = plt.subplot(1,1,1)
        cm = []
        for leg in range(4):
            # draw the feet that are on the ground
            if feet[leg][step][2] < -62:
                plt.plot(
                    [body[leg][0],feet[leg][step][0]],
                    [body[leg][1],feet[leg][step][1]],
                    label='Leg[{}]'.format(leg),
                    marker='o'
                )
                cm.append(feet[leg][step])  # save to calculat cm position
            else:
                plt.plot(
                    [body[leg][0],feet[leg][step][0]],
                    [body[leg][1],feet[leg][step][1]],
                    label='Leg[{}]'.format(leg),
                    marker='o',
                    linestyle=':',
                    alpha=0.5
                )
#         x = 0
#         y = 0
#         for p in cm:
#             x += p[0]
#             y += p[1]
#         x /= len(cm)
#         y /= len(cm)
#         plt.plot([x],[y],color='y', marker='^')  # center mass
        plt.plot([0],[0],color='y', marker='^', label='Center Mass')  # center mass

        plt.title('Step {}'.format(step))
        plt.grid(True)
#         plt.plot([x[0] for x in body], [y[1] for y in body], label='Body', marker='o')
        rect = plt.Rectangle(
            body[3],  # lower left corner
            body[1][0] - body[2][0],  # width
            body[1][1] - body[0][1],  # height
            color='k')
        ax.add_patch(rect)
#         ax.axis([-200,200,-200,200])
        ax.axis('equal')
        plt.pause(pause)
        # plt.show()

    # plt.legend();
    plt.show()
