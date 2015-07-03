#!/usr/bin/python
#
# An implementation of a Loop Erased Random Walk (LERW)
# from a cylinder with reflecting boundaries on the left
# and open boundaries on the right.
# PNG output of a single trajectory.
# Habib Rehmann and Gunnar Pruessner
#

import random
import matplotlib.mlab as mlab
import numpy as np
import matplotlib.pyplot as plt
from itertools import groupby

seed = 10  # random seed
Length = 200  # length of the cyclinder
Circ = 200  # circumference of cyclinder
x = 0   # x coordinate of starting location
# y coordinate of starting location. Origin is at centre of square
y = Circ / 2
s = 0  # Step number.
nLE = []  # number of loops erased for coordinate

trajectory = []   # List of the x coordinates of all points visited.
# (Length x Circ) 2D array of zeros
lattice = np.zeros((Length, Circ), dtype=int)
random.seed(seed)

# Generate a randomwalk
while True:
    s += 1
    if (bool(random.getrandbits(1))):
        if (bool(random.getrandbits(1))):
            x += 1
        else:
            x -= 1
    else:
        if (bool(random.getrandbits(1))):
            y += 1
        else:
            y -= 1

    if (x >= Length):
        break
    elif (x < 0):
        x = 0
    if (y >= Circ):
        y -= Circ
    elif (y < 0):
        y += Circ

    lattice[x][y] += 1
    trajectory.append((x, y))

x0 = None
y0 = None
pos = 0

# Loop erasure
while pos < len(trajectory):
    x, y = trajectory[pos]
    if lattice[x][y] > 1 and (not x0):
        x0, y0 = x, y
        pos0 = pos
    elif (x == x0) and (y == y0) and (lattice[x][y] == 1):
        del trajectory[pos0:pos]
        nLE.append(pos - pos0 - 1)
        x0, y0 = None, None
        pos = pos0
    lattice[x][y] -= 1
    pos += 1

nLE = np.array(nLE)

# Distribution of number of loops erased with repect to displacement histogram
# nLE = x: number of loops erased for coordinate

# Normalized distribution
# mu, sigma = np.mean(nLE), np.std(nLE)
# x = [((mu - x)/sigma) for x in nLE]
x = nLE

# the histogram of the data
n, bins, patches = plt.hist(x, 70, normed=1, facecolor='green', alpha=0.75)

plt.xlabel('Number of loops erased for coordinate')
plt.ylabel('Frequency')
plt.title(r'$\mathrm{Histogram\ of\ normalized\ LERW:}\ $')
plt.grid(True)


plt.savefig("LEnum_distr_histogram.png", bbox_inches="tight")
