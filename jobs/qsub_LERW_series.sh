#!/bin/sh
## one day
#PBS -l walltime=15:00:00
#PBS -l mem=1000mb
#PBS -l ncpus=1

cd $PBS_O_WORKDIR

echo script $0
pwd
hostname
date
s=30001
for L in 50 100 200 400
do
  s=$(( $s + 5 ))
  time ./LERW_cluster_sizes.py -i 100000 -L $L -C $L -s $s > LERW_cluster_sizes_${L}.dat 2>&1 
done
date
