#!/usr/bin/python
#
# Escape time of a random walker from a cylinder with reflecting
# boundaries on the left and open boundaries on the right
# Habib Rehmann and Gunnar Pruessner
#
#

import random
from numpy import cos, sin, radians
import numpy as np
import matplotlib.pyplot as plt

seed = 7
Length = 10 # length of the cyclinder
Circ = 20 # circumference of cyclinder
Iterations = 20000




xStart = 0   # x coordinate of starting location. Origin is at centre of square
yStart = Circ/2

random.seed(seed) # set random seed

m0=0
m1=0

for it in range(1, Iterations+1):
  s = 0  # Step number.
  x = xStart   # x coordinate of point.
  y = yStart   # y coordinate of point.

  while True:
    if (bool(random.getrandbits(1))):
      if (bool(random.getrandbits(1))):
	x+=1
      else:
	x-=1
    else:
      if (bool(random.getrandbits(1))):
	y+=1
      else:
	y-=1

    s += 1
    if (x>=Length):
      break;
    if (x<0): 
      x=0
    if (y>=Circ):
      y-=Circ
    if (y<0):
      y+=Circ

  m0+=1
  m1+=s

print(m0, float(m1)/float(m0))