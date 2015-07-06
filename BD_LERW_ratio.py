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

intr = []
randomwalk = LERW()
randomwalk.gen_bidirectional(realizations=5, Length=200, Circ=200)
LERW_LeftRight = randomwalk.trajectories_leftright
LERW_RightLeft = randomwalk.trajectories_rightleft

for i in range(len(LERW_RightLeft)):
    intersection = set(LERW_LeftRight[i]).intersection(LERW_RightLeft[i])
    if intersection:
        intr.append(intersection)



# Distribution of the horizontal displacement of the intersections
    # x = np.array([x[0] for i in range(len(intr)) for x in intr[i]])

print("The ratio of number intersections to the total number of coordinates is {}:{} = {}".format(len(intr), len(LERW_RightLeft), float(len(intr)/len(LERW_RightLeft))))
