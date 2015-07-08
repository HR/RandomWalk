#!/usr/bin/python
#
# An implementation of a Loop Erased Random Walk (LERW)
# from a cylinder with reflecting boundaries on the left
# and open boundaries on the right.
# PNG output of a single trajectory.
# Habib Rehmann and Gunnar Pruessner
#


import numpy as np
import matplotlib.pyplot as plt
from LERW import LERW
import itertools

# https://docs.python.org/2/howto/argparse.html
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--seed", type=int, help="seed of the RNG", default=7)
parser.add_argument("-L", "--Length", type=int, help="length of the system", default=200)
parser.add_argument("-C", "--Circ", type=int, help="Circ of the system (PBC apply)", default=200)
parser.add_argument("-i", "--iterations", type=int, help="iterations", default=100)
args = parser.parse_args()


print "# Info: seed = ", args.seed
print "# Info: Length = ", args.Length
print "# Info: Circ = ", args.Circ
print "# Info: iterations = ", args.iterations
 

randomwalk = LERW(seed=args.seed)
randomwalk.generate(realizations=args.iterations, Length=args.Length, Circ=args.Circ)
ELsizes = randomwalk.ErasedLoopSizes
x = list(itertools.chain(*ELsizes))

for s in list(itertools.chain(*ELsizes)):
   print s
