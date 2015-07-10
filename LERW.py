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
from copy import deepcopy

class LERW:
	def __init__(self, **kwargs):
		self.seed = kwargs.get('seed', 10) # random seed
		self.trajectories = [] # List of the coordinates of all points visited.
		self.ErasedLoopSizes = [] # List of the sizes of the erased loops

	def generate(self, **kwargs):
		self.Length = kwargs.get('Length', 200) # length of the cyclinder
		self.Circ = kwargs.get('Circ', 200) # circumference of cyclinder
		self.realizations = kwargs.get('realizations', 1) # length of the cyclinder
		random.seed(self.seed)

		for i in range(self.realizations):
			s = 0
			x = 0 # x coordinate of starting location
			y = self.Circ / 2 # y coordinate of starting location
			lattice = np.zeros((self.Length, self.Circ), dtype=int)
			trajectory = []
			ELsize = []

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

				if (x >= self.Length):
					break
				elif (x < 0):
					x = 0
				if (y >= self.Circ):
					y -= self.Circ
				elif (y < 0):
					y += self.Circ

				lattice[x][y] += 1
				trajectory.append((x, y))

			x0, y0, pos = None, None, 0


			# Loop erasure
			while pos < len(trajectory):
				x, y = trajectory[pos]
				if lattice[x][y] > 1 and (not x0):
					x0, y0 = x, y
					pos0 = pos
				elif (x == x0) and (y == y0) and (lattice[x][y] == 1):
					del trajectory[pos0:pos]
					ELsize.append(pos - pos0 - 1)
					x0, y0 = None, None
					pos = pos0
				lattice[x][y] -= 1
				pos += 1
			self.ErasedLoopSizes.append(ELsize)
			self.trajectories.append(trajectory)

	def gen_bidirectional(self, **kwargs):
		self.Length = kwargs.get('Length', 200) # length of the cyclinder
		self.Circ = kwargs.get('Circ', 200) # circumference of cyclinder
		self.realizations = kwargs.get('realizations', 1) # length of the cyclinder
		self.trajectories_leftright = []
		self.trajectories_rightleft = []
		random.seed(self.seed)

		for i in range(self.realizations):
			s = 0
			x = 0 # x coordinate of starting location
			y = self.Circ / 2 # y coordinate of starting location
			lattice = np.zeros((self.Length, self.Circ), dtype=int)
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

				if (x >= self.Length):
					break
				elif (x < 0):
					x = 0
				if (y >= self.Circ):
					y -= self.Circ
				elif (y < 0):
					y += self.Circ

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

			self.trajectories_leftright.append(LERW_LeftRight)
			self.trajectories_rightleft.append(LERW_RightLeft)

	def gen_fromCoord(self, **kwargs):
		self.Length = kwargs.get('Length', 200) # length of the cyclinder
		self.Circ = kwargs.get('Circ', 200) # circumference of cyclinder
		self.realizations = kwargs.get('realizations', 1) # length of the cyclinder
		random.seed(self.seed)
		xStart = kwargs.get('xStart', random.randint(0, self.Length))
		yStart = kwargs.get('yStart', random.randint(0, self.Length))
		x, y = xStart, yStart

		for i in range(self.realizations):
			s = 0
			x, y = xStart, yStart
			lattice = np.zeros((self.Length, self.Circ), dtype=int)
			trajectory = []
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
				if (x >= self.Length):
					x -= self.Length
				elif (x < 0):
					x += self.Length
				if (y >= self.Circ):
					y -= self.Circ
				elif (y < 0):
					y += self.Circ

				if (x == xStart and y == yStart):
					break

				lattice[x][y] += 1
				trajectory.append((x, y))

			self.trajectories.append(trajectory)

	@property
	def trajectories(self):
		return self.trajectories

	@property
	def ErasedLoopSizes(self):
		return self.ErasedLoopSizes

	@property
	def trajectories_rightleft(self):
		return self.trajectories_rightleft

	@property
	def trajectories_leftright(self):
		return self.trajectories_leftright

	def plot(self, **kwargs):
		LERW = kwargs.get('LERW', self.trajectories)
		c = kwargs.get('c', 'g')
		Length = kwargs.get('Length', self.Length)
		Circ = kwargs.get('Circ', self.Circ)
		figname = kwargs.get('figname', 'LERW_output')

		fig, ax = plt.subplots()
		fig.set_size_inches(3, self.Circ * 3. / self.Length)
		ax.set_xlim(0, self.Length - 1)
		ax.set_ylim(0, self.Circ - 1)
		ax.get_xaxis().set_visible(False)
		ax.get_yaxis().set_visible(False)

		for pos in range(len(LERW)):
			x, y = LERW[pos]
			if (x == Length) or (x == 0) or (y == Circ) or (y == Circ) or (y == 0):
				LERW[pos] = (np.nan, np.nan)
			pos += 1

		plt.plot(*zip(*LERW), color=c, linewidth=0.2)
		plt.savefig(figname, bbox_inches='tight', dpi=kwargs.get('dpi', 300))
