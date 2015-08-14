#!/usr/bin/python
#
# An implementation of a Bidirectional Loop Erased Random Walk (LERW)
# from a cylinder with reflecting boundaries on the left
# and open boundaries on the right.
# PNG output of a single trajectory
# Distribution of the displacement of the intersections
# Habib Rehmann and Gunnar Pruessner
#

import numpy as np
import matplotlib.pyplot as plt
from LERW import LERW

n = 1
length = 20
areas = [] # list of intersections' enclosed area

randomwalk = LERW()
randomwalk.gen_bidirectional(realizations=n, Length=length, Circ=20)
LERW_LeftRight = randomwalk.trajectories_leftright[0]
LERW_RightLeft = randomwalk.trajectories_rightleft[0]
# Calc: enclosed area between the intersections of bidirectional random walks


for i in range(length):
    lr = [x for j, x in enumerate(LERW_LeftRight) if x[0] == i]
    rl = [x for j, x in enumerate(LERW_RightLeft) if x[0] == i]
    
    if len(lr) > 1 or len(rl) > 1:
        print("At {}:\n\tleft-right: {}, \n\tright-left: {}".format(i, lr, rl))
#
# print areas



# Plot random walk
# plt.savefig(__file__[:-3]+".png", bbox_inches="tight", dpi=250)
