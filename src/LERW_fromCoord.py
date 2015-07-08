#!/usr/bin/python
#
# An implementation of a Loop Erased Random Walk (LERW)
# from a cylinder with reflecting boundaries on the left
# and open boundaries on the right.
# PNG output of a single trajectory.
# Habib Rehmann and Gunnar Pruessner
#

import random
import numpy as np
import matplotlib.pyplot as plt

seed = 10  # random seed
Length = 20  # length of the cyclinder
Circ = 20  # circumference of cyclinder
s = 0  # Step number.

trajectory = []   # List of the x coordinates of all points visited.
# (Length x Circ) 2D array of zeros
lattice = np.zeros((Length, Circ), dtype=int)
random.seed(seed)

xStart = random.randint(0, Length)	# x coordinate of starting location
yStart = random.randint(0, Length)	# y coordinate of starting location
x, y = xStart, yStart

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

	# Periodic boundaries
	if (x >= Length):
		x -= Length
	elif (x < 0):
		x += Length
	if (y >= Circ):
		y -= Circ
	elif (y < 0):
		y += Circ

	if (x == xStart and y == yStart):
		break

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
		x0, y0 = None, None
		pos = pos0
	lattice[x][y] -= 1
	pos += 1

# Plot random walk
dpi = 300
fig, ax = plt.subplots()
fig.set_size_inches(3, Circ * 3. / Length)
ax.set_xlim(0, Length - 1)
ax.set_ylim(0, Circ - 1)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
plt.plot(*zip(*trajectory), marker=".",linewidth=0.3)
plt.savefig(__file__[:-3]+".png", bbox_inches="tight", dpi=dpi)
