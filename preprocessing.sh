#!/bin/bash -l 

#PBS -N model_preprocessing
#PBS -A NAML0001
#PBS -l walltime=12:00:00
#PBS -l select=1:ncpus=4:ngpus=0:mem=64GB
#PBS -q casper
#PBS -j oe

source ~/.bashrc
conda activate winter-ptype

python preprocessing.py