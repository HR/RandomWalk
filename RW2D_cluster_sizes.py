#!/usr/bin/python
#
# Escape time of a random walker from a cylinder with reflecting
# boundaries on the left and open boundaries on the right.
# PNG output of a single trajectory.
# Habib Rehmann and Gunnar Pruessner
#

import random


# 200x200 with 200 realisations take about 50s on yangtze

# https://docs.python.org/2/howto/argparse.html
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--seed", type=int, help="seed of the RNG", default=7)
parser.add_argument("-L", "--Length", type=int, help="length of the system (PBC apply)", default=200)
parser.add_argument("-C", "--Circ", type=int, help="Circ of the system (PBC apply)", default=200)
parser.add_argument("-i", "--iterations", type=int, help="iterations", default=100)
args = parser.parse_args()


print "# Info: seed = ", args.seed
print "# Info: Length = ", args.Length
print "# Info: Circ = ", args.Circ
print "# Info: iterations = ", args.iterations

xStart = 0   # x coordinate of starting location. Origin is at centre of square
yStart = args.Circ / 2

random.seed(args.seed)  # set random seed
for i in range(args.iterations):
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

      if (x >= args.Length):
	  x -= args.Length
      if (x < 0):
	  x += args.Length
      if (y >= args.Circ):
	  y -= args.Circ
      if (y < 0):
	  y += args.Circ

      if ((x==xStart) and (y==yStart)):
      	print s
	break

