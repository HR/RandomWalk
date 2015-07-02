#!/usr/bin/python
#
# An implementation of a Bidirectional Loop Erased Random Walk (LERW)
# from a cylinder with reflecting boundaries on the left
# and open boundaries on the right.
# PNG output of a single trajectory.
# Habib Rehmann and Gunnar Pruessner
#

import random
from numpy import cos, sin, radians
import numpy as np
import matplotlib.pyplot as plt

seed = 10 # random seed
Length = 200  # length of the cyclinder
Circ = 200  # circumference of cyclinder
x = 0   # x coordinate of starting location
y = Circ / 2 # y coordinate of starting location. Origin is at centre of square
s = 0  # Step number.

trajectory = []   # List of the x coordinates of all points visited.
lattice = np.zeros((Length, Circ), dtype=int) # (Length x Circ) 2D array of zeros
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

dpi = 300
fig, ax = plt.subplots()
fig.set_size_inches(3, Circ * 3. / Length)
ax.set_xlim(0, Length - 1)
ax.set_ylim(0, Circ - 1)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)

plt.plot(*zip(*trajectory), color='r',linewidth=0.3)

x0 = None
y0 = None
pos = 0
lerw = trajectory[:]
lcpy = lattice[:][:]
print 'Length: ', len(lerw)
print [lerw[0], lerw[len(lerw)-1]]
print 'lattice[0][97]: ', lattice[0][97]
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
        print 'Loop 1 delete from ', pos0, ' to ', pos
        x0, y0 = None, None
        pos = pos0
    lcpy[x][y] -= 1
    pos += 1

plt.plot(*zip(*lerw), color='b',linewidth=0.3)

lerw = trajectory[::-1]
print 'Length: ', len(lerw)

print [lerw[0], lerw[len(lerw)-1]]
print 'lattice[0][97]: ', lattice[0][97]

lcpy=lattice[:][:]
x0 = None
y0 = None
pos=0
while pos < len(lerw):
    x, y = lerw[pos]
    print x, y, lcpy[x][y]
    if lcpy[x][y] > 1 and (not x0):
        x0, y0 = x, y
        pos0 = pos
        print("First repeated element ", pos0, x0, y0)
    elif (x == x0) and (y == y0) and (lcpy[x][y] == 1):
        # print("Deleting from ", pos0, " to ", pos)
        del lerw[pos0:pos]
        print 'Loop 2 delete from ', pos0, ' to ', pos
        x0, y0 = None, None
        pos = pos0
    lcpy[x][y] -= 1
    pos += 1

plt.plot(*zip(*lerw), color='g',linewidth=0.3)

# Plot random walk
plt.savefig("RandomWalk.png", bbox_inches="tight", dpi=dpi)
