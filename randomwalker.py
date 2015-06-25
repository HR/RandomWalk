
#!/usr/bin/python
#
# Escape time of a random walker from a cylinder with reflecting
# boundaries on the left and open boundaries on the right. 
# PNG output of a single trajectory.
# Habib Rehmann and Gunnar Pruessner
#
#

import random
from numpy import cos, sin, radians
import numpy as np
import matplotlib.pyplot as plt

seed = 7
N = 1   # Stepsize
Length = 40 # length of the cyclinder
Circ = 20 # circumference of cyclinder
xStart = 0   # x coordinate of starting location. Origin is at centre of square
yStart = Circ/2

s = 0  # Step number.
x = xStart   # x coordinate of point.
y = yStart   # y coordinate of point.
xList = []   # List of the x coordinates of all points visited.
yList = []   # List of the y coordinates of all points visited.
lattice = np.zeros((Circ, Length), dtype=int) # (Length x Circ) 2 dimensional array prepopulated by zeros

random.seed(seed) # set random seed


# Generate a randomwalk
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

	lattice[y][x] += 1
	xList.append(x)
	yList.append(y)

x0 = -1
y0 = -1
c = 0
pos = 0

print(len(xList))

# Erase loops
for y in yList:
	x = xList[pos]
	#print(lattice[4][8],x,x0,y,y0)
	#if lattice[y][x] > 1:
		#print("({}, {}) visited {} times".format(x, y, lattice[y][x]))
	if lattice[y][x] > 1 and (x0 == -1):
		x0 = x
		y0 = y
		pos0 = pos
		print("{}, {} coordinate at pos {}, {}".format(x, y, pos, lattice[y][x]))
	elif (x == x0) and (y == y0) and (lattice[y][x]==1):
		# erase loop
		try:	
			del xList[pos0:pos0+c+1]
			del yList[pos0:pos0+c+1]
		except ValueError:
			print("x: {}, y: {}, c: {}".format(x, y, c))
		x0, y0 = -1, -1
		pos-=(c+1)
		print(pos, c, x, y)
		c = 0
		print(len(xList))
	else:
		c += 1
	lattice[y][x] -= 1
	pos+=1

# Plot random walk
# from http://stackoverflow.com/questions/16057869/setting-the-size-of-the-plotting-canvas-in-matplotlib
# and Habib suggesting using set_size_inches
## dpi=72.
## ax.plot(xList,yList,'r,')

dpi=300
## xinch = Length / dpi
## yinch = Circ / dpi


fig, ax = plt.subplots()
fig.set_size_inches(2,3)
## fig.set_size_inches(xinch,yinch);
ax.plot(xList,yList, ".")
## ax.plot(xList,yList,'r.')
ax.set_xlim(0, Length-1)
ax.set_ylim(0, Circ-1)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
plt.savefig("randomWalk.png", bbox_inches="tight", dpi=dpi)
