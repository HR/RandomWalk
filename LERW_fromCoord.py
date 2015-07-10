#!/usr/bin/python
#
# An implementation of a Loop Erased Random Walk (LERW)
# from a cylinder with reflecting boundaries on the left
# and open boundaries on the right.
# PNG output of a single trajectory.
# Habib Rehmann and Gunnar Pruessner
#


import numpy as np
import matplotlib.pyplot as plt
import random
from LERW import LERW
import itertools


randomwalk = LERW()
randomwalk.gen_fromCoord(realizations=8, Length=200, Circ=200)
# x = np.array(x)

for walk in randomwalk.trajectories:
    randomwalk.plot(LERW=walk, c=random.choice(['b', 'g', 'r', 'c', 'm', 'y', 'k']))

# Distribution of size of loops erased with repect to displacement histogram

# the histogram of the data
# n, bins, patches = plt.hist(x, bins=150, normed=1, facecolor='green', alpha=0.75)
#
# plt.xlabel('Size of loops erased for coordinate')
# plt.ylabel('Frequency')
# plt.yscale('log', nonposy='clip')
# plt.xscale('log', nonposy='clip')
# # plt.loglog(x, basex=2)
# plt.title(r'$\mathrm{Histogram\ of\ the\ horizontal\ displacement\ distribution:}\ $')
# plt.grid(True)
#
# plt.savefig("plots/"+__file__[:-3]+"_histogram.png", bbox_inches="tight")
