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
Length = 200  # length of the cyclinder
xStart = 0   # x coordinate of starting location. Origin is at centre of square

random.seed(seed)  # set random seed
for i in range(5000):
  x = xStart   # x coordinate of point.

  # Generate a randomwalk
  s=0
  while True:
      s += 1
      if (bool(random.getrandbits(1))):
        x += 1
      else:
	x -= 1
      if (x >= Length):
	  x -= Length
      if (x < 0):
	  x += Length
      if (x==xStart):
      	print s
	break

