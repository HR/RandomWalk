#!/usr/bin/python
#
# An implementation of a Bidirectional Loop Erased Random Walk (LERW)
# from a cylinder with reflecting boundaries on the left
# and open boundaries on the right.
# PNG output of a single trajectory.
# Habib Rehmann and Gunnar Pruessner
#

import random
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

seed = 10  # random seed
Length = 200  # length of the cyclinder
Circ = 200  # circumference of cyclinder
x = 0   # x coordinate of starting location
# y coordinate of starting location. Origin is at centre of square
y = Circ / 2
s = 0  # Step number.

trajectory = []   # List of the x coordinates of all points visited.
# (Length x Circ) 2D array of zeros
lattice = np.zeros((Length, Circ), dtype=int)
random.seed(seed)

# Plot config
dpi = 300
fig, ax = plt.subplots()
fig.set_size_inches(3, Circ * 3. / Length)
ax.set_xlim(0, Length - 1)
ax.set_ylim(0, Circ - 1)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)

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

plt.plot(*zip(*trajectory), color='r', linewidth=0.3)

x0 = None
y0 = None
pos = 0
lerw = deepcopy(trajectory)
lcpy = deepcopy(lattice)
# Loop erasure (tranversal from left to right)
while pos < len(lerw):
    x, y = lerw[pos]
    if lcpy[x][y] > 1 and (not x0):
        x0, y0 = x, y
        pos0 = pos
        # print("First repeated element ", pos0, x0, y0)
    elif (x == x0) and (y == y0) and (lcpy[x][y] == 1):
        # print("Deleting from ", pos0, " to ", pos)
        del lerw[pos0:pos]
        # print 'Loop 1 delete from ', pos0, ' to ', pos
        x0, y0 = None, None
        pos = pos0
    lcpy[x][y] -= 1
    pos += 1

plt.plot(*zip(*lerw), color='b', linewidth=0.3)

lerw = deepcopy(trajectory[::-1])
lcpy = deepcopy(lattice)
x0 = None
y0 = None
pos = 0
while pos < len(lerw):
    x, y = lerw[pos]
    if lcpy[x][y] > 1 and (not x0):
        x0, y0 = x, y
        pos0 = pos
    elif (x == x0) and (y == y0) and (lcpy[x][y] == 1):
        # print("Deleting from ", pos0, " to ", pos)
        del lerw[pos0:pos]
        x0, y0 = None, None
        pos = pos0
    lcpy[x][y] -= 1
    pos += 1

plt.plot(*zip(*lerw), color='g', linewidth=0.3)

# Plot random walk
plt.savefig(__file__[:-3]+".png", bbox_inches="tight", dpi=dpi)
