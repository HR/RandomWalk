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
randomwalk.gen_bidirectional(realizations=100, Length=200, Circ=200)
LERW_LeftRight = randomwalk.trajectories_leftright
LERW_RightLeft = randomwalk.trajectories_rightleft
# plt.plot(*zip(*lerwrl), color='g', linewidth=0.3)
for i in range(len(LERW_RightLeft)):
    intr.append(list(set(LERW_LeftRight[i]).intersection(LERW_RightLeft[i])))



# Distribution of the horizontal displacement of the intersections
x = np.array([x[0] for i in range(len(intr)) for x in intr[i]])
n, bins, patches = plt.hist(x, 70, normed=1, facecolor='green', alpha=0.75)

plt.xlabel('Horizontal displacement')
plt.ylabel('Frequency')
plt.title(r'$\mathrm{Distribution\ of\ the\ horizontal\ displacement\ of\ the\ intersections:}\ $')
plt.grid(True)

plt.savefig(__file__[:-3]+"_(horiz_dis).png", bbox_inches="tight")

# Distribution of the vertical displacement of the intersections

# n, bins, patches = plt.hist(x, 70, normed=1, facecolor='green', alpha=0.75)
#
# plt.xlabel('Vertical displacement')
# plt.ylabel('Frequency')
# plt.title(r'$\mathrm{Distribution\ of\ the\ vertical\ displacement\ of\ the\ intersections:}\ $')
# plt.grid(True)
#
# # Plot random walk
# plt.savefig(__file__[:-3]+"_(verti_dis).png", bbox_inches="tight")
