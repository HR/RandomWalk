#!/usr/bin/python
#
# Escape time of a random walker from a cylinder with reflecting
# boundaries on the left and open boundaries on the right. 
# PNG output of a single trajectory.
# Habib Rehmann and Gunnar Pruessner
#
# $Header: /home/ma/p/pruess/.cvsroot/misc/randomwalkv4.py,v 1.1 2015/06/19 13:30:11 pruess Exp $
#

import random
from numpy import cos, sin, radians
import numpy as np
import matplotlib.pyplot as plt

seed = 7
N = 1   # Stepsize
Length = 400 # length of the cyclinder
Circ = 200 # circumference of cyclinder
xStart = 0   # x coordinate of starting location. Origin is at centre of square
yStart = Circ/2

s = 0  # Step number.
x = xStart   # x coordinate of point.
y = yStart   # y coordinate of point.
xList = []   # List of the x coordinates of all points visited.
yList = []   # List of the y coordinates of all points visited.

random.seed(seed) # set random seed

while True:
  s += 1
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

  if (x>=Length):
    break;
  if (x<0): 
    x=0
  if (y>=Circ):
    y-=Circ
  if (y<0):
    y+=Circ

  xList.append(x)
  yList.append(y)

# from
# http://stackoverflow.com/questions/16057869/setting-the-size-of-the-plotting-canvas-in-matplotlib
# and Habib suggesting using set_size_inches
dpi=72.
xinch = Length / dpi
yinch = Circ / dpi

fig, ax = plt.subplots()
fig.set_size_inches(xinch,yinch);
ax.plot(xList,yList,'r,')
ax.set_xlim(0, Length-1)
ax.set_ylim(0, Circ-1)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
plt.savefig("randomWalk.png", bbox_inches="tight", dpi=dpi)
