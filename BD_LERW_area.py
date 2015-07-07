#!/usr/bin/python
#
# An implementation of a Bidirectional Loop Erased Random Walk (LERW)
# from a cylinder with reflecting boundaries on the left
# and open boundaries on the right.
# PNG output of a single trajectory
# Distribution of the displacement of the intersections
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

# plt.plot(*zip(*trajectory), color='r', linewidth=0.3)


# Loop erasure (tranversal from left to right)
lerwlr = deepcopy(trajectory)
lcpy = deepcopy(lattice)
x0, y0 = None, None
pos = 0

while pos < len(lerwlr):
	x, y = lerwlr[pos]
	if lcpy[x][y] > 1 and (not x0):
		x0, y0 = x, y
		pos0 = pos
	elif (x == x0) and (y == y0) and (lcpy[x][y] == 1):
		del lerwlr[pos0:pos]
		x0, y0 = None, None
		pos = pos0
	lcpy[x][y] -= 1
	pos += 1

# plt.plot(*zip(*lerwlr), color='b', linewidth=0.3)


# Loop erasure (tranversal from right to left)
lerwrl = deepcopy(trajectory[::-1])
lcpy = deepcopy(lattice)
x0, y0 = None, None
pos = 0

while pos < len(lerwrl):
	x, y = lerwrl[pos]
	if lcpy[x][y] > 1 and (not x0):
		x0, y0 = x, y
		pos0 = pos
	elif (x == x0) and (y == y0) and (lcpy[x][y] == 1):
		del lerwrl[pos0:pos]
		x0, y0 = None, None
		pos = pos0
	lcpy[x][y] -= 1
	pos += 1

# plt.plot(*zip(*lerwrl), color='g', linewidth=0.3)


# Determine the enclosed area between the bidirectional random walks
areas = []

for i in range(Circ):
	for x in lerwlr:
		if x[1] == i:

print areas



# Plot random walk
# plt.savefig(__file__[:-3]+"_(verti_dis).png", bbox_inches="tight")
