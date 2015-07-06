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

randomwalk = LERW()
randomwalk.generate(realizations=50, Length=200, Circ=200)
ELsizes = randomwalk.ErasedLoopSizes
ELsizes = list(map(list, zip(*ELsizes)))
x = []

for i in range(len(ELsizes)):
    x.append(np.mean(ELsizes[i]))
x = np.array(x)
# Distribution of size of loops erased with repect to displacement histogram

# the histogram of the data
n, bins, patches = plt.hist(x, 80, normed=1, facecolor='green', alpha=0.75)

plt.xlabel('Size of loops erased for coordinate')
plt.ylabel('Frequency')
plt.title(r'$\mathrm{Histogram\ of\ the\ horizontal\ displacement\ distribution:}\ $')
plt.grid(True)

plt.savefig(__file__[:-3]+"_histogram.png", bbox_inches="tight")

# x = [ pow(10,i) for i in x]
plt.yscale('log')
plt.xscale('log')
plt.subplot(223)
plt.title(r'$\mathrm{Double\ logarithmic\ (scales)\ plot\ for\ distribution:}\ $')
plt.grid(True)
plt.loglog(x, pow(x, 10) , basex=2)
plt.savefig(__file__[:-3]+"_loglog.png", bbox_inches="tight", dpi=200)
