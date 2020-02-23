#!/usr/bin/env python3

from robot import Tripod
from params import spider
from pprint import pprint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

t = Tripod(spider["neutral"], 25, 20)

# pprint(t.gait)
gait = t.gait

m = 'h'
for leg, c, i in zip(gait, ['b','g','r','c','m','y'],[1,2,3,4,5,6]):
    x = [n[0] for n in leg] + [leg[0][0]]
    y = [n[1] for n in leg] + [leg[0][1]]
    z = [n[2] for n in leg] + [leg[0][2]]
    ax.plot(x[:1],y[:1],z[:1],marker="h",c="k",markersize=15)
    ax.plot(x,y,z,"-h",c=c,label=f"Leg {i}: {len(x)} pts")

ax.set_xlabel('X [mm]')
ax.set_ylabel('Y [mm]')
ax.set_zlabel('Z [mm]')
ax.legend()
# ax.set_aspect('equal', 'box')

plt.show()
