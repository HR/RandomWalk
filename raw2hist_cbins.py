#!/usr/bin/python
#
# An implementation of a Bidirectional Loop Erased Random Walk (LERW)
# from a cylinder with reflecting boundaries on the left
# and open boundaries on the right.
# PNG output of a single trajectory
# Distribution of the displacement of the intersections
# Habib Rehmann and Gunnar Pruessner
#
import numpy as np
import matplotlib.pyplot as plt
from LERW import LERW
import subprocess
import os

dpath = "data/qsub/"
spath = "plots/hist/cbins/"
p = subprocess.Popen(['ls', '-v', dpath], stdout=subprocess.PIPE)
fnames = p.communicate()[0].split('\n')[:-1]
fname = "LERW_cluster_sizes_50.dat"

for fname in fnames:
    p = subprocess.Popen(['./craw2binned', '-f', dpath+fname], stdout=subprocess.PIPE)
    bins = p.communicate()[0].split('\n')[:-1]
    x, y = [], []
    for coord in bins:
        x.append(coord.split('\t')[0])
        y.append(coord.split('\t')[1])
    x, y = np.array(x), np.array(y)


    # Distribution of cluster sizes
    #n, bins, patches = plt.hist(x, 70, normed=1, facecolor='green', alpha=0.75)

    plt.yscale('log', nonposy='clip')
    plt.xscale('log', nonposy='clip')
    plt.xlabel('Cluster size (sys size: {})'.format(fname[-6:-4]))
    plt.ylabel('Frequency')
    plt.title(r'$\mathrm{'+fname[:-4].replace('_', '\ ')+':}\ $')
    plt.grid(True)
    plt.plot(x, y)

    plt.savefig(spath+fname[:-4]+"_histogram.png", bbox_inches="tight")
