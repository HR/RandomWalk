#!/usr/bin/python
#
# Escape time of a random walker from a cylinder with reflecting
# boundaries on the left and open boundaries on the right.
# PNG output of a single trajectory.
# Habib Rehmann and Gunnar Pruessner
#

import random
from numpy import cos, sin, radians
import numpy as np
import matplotlib.pyplot as plt

seed = 7
N = 1   # Stepsize
Length = 200  # length of the cyclinder
Circ = 200  # circumference of cyclinder
xStart = 0   # x coordinate of starting location. Origin is at centre of square
yStart = Circ / 2

# 200x200 with 200 realisations take about 50s on yangtze

random.seed(seed)  # set random seed
for i in range(5000):
  x = xStart   # x coordinate of point.
  y = yStart   # y coordinate of point.

  # Generate a randomwalk
  s=0
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
	  x -= Length
      if (x < 0):
	  x += Length
      if (y >= Circ):
	  y -= Circ
      if (y < 0):
	  y += Circ

      if ((x==xStart) and (y==yStart)):
      	print s
	break

