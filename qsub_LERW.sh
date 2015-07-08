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
time ./LERW_horizontal_displacement_distribution.py > LERW_horizontal_displacement_distribution.dat 2>&1 
date
