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
realizations = 8

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

def plot(LERW, c='g', Length = Length, Circ = Circ):
	for pos in range(len(LERW)):
		x, y = LERW[pos]
		if (x == Length) or (x == 0) or (y == Circ) or (y == Circ) or (y == 0):
			LERW[pos] = (np.nan, np.nan)
		pos += 1
	plt.plot(*zip(*LERW), color=c, linewidth=0.2)

# Generate a randomwalk
for i in range(realizations):
	s = 0
	x = 0 # x coordinate of starting location
	y = Circ / 2 # y coordinate of starting location
	lattice = np.zeros((Length, Circ), dtype=int)
	trajectory = []

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

	x0, y0, pos = None, None, 0


	# Loop erasure
	LERW_LeftRight = deepcopy(trajectory)
	lcpy = deepcopy(lattice)
	x0, y0 = None, None
	pos = 0

	while pos < len(LERW_LeftRight):
		x, y = LERW_LeftRight[pos]
		if lcpy[x][y] > 1 and (not x0):
			x0, y0 = x, y
			pos0 = pos
		elif (x == x0) and (y == y0) and (lcpy[x][y] == 1):
			del LERW_LeftRight[pos0:pos]
			x0, y0 = None, None
			pos = pos0
		lcpy[x][y] -= 1
		pos += 1


	plot(LERW_LeftRight)

	# Loop erasure (tranversal from right to left)
	LERW_RightLeft = deepcopy(trajectory[::-1])
	lcpy = deepcopy(lattice)
	x0, y0 = None, None
	pos = 0

	while pos < len(LERW_RightLeft):
		x, y = LERW_RightLeft[pos]
		if lcpy[x][y] > 1 and (not x0):
			x0, y0 = x, y
			pos0 = pos
		elif (x == x0) and (y == y0) and (lcpy[x][y] == 1):
			del LERW_RightLeft[pos0:pos]
			x0, y0 = None, None
			pos = pos0
		lcpy[x][y] -= 1
		pos += 1

	plot(LERW_RightLeft, 'r')



# Plot random walk
plt.savefig(__file__[:-3]+".png", bbox_inches="tight", dpi=dpi)
