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
length = 200
areas = [] # list of intersections' enclosed area

randomwalk = LERW()
randomwalk.gen_bidirectional(realizations=n, Length=length, Circ=200)
LERW_LeftRight = randomwalk.trajectories_leftright
LERW_RightLeft = randomwalk.trajectories_rightleft

# Calc: enclosed area between the intersections of bidirectional random walks


# for i in range(length):
# 	for x in lerwlr:
# 		if x[1] == i:
#
# print areas



# Plot random walk
# plt.savefig(__file__[:-3]+".png", bbox_inches="tight", dpi=250)
