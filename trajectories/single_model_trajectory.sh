#!/bin/bash -l 

#PBS -N sm_trajectory
#PBS -A NAML0001
#PBS -l walltime=12:00:00
#PBS -l select=1:ncpus=1:ngpus=0:mem=32GB
#PBS -q casper
#PBS -j oe

source ~/.bashrc
conda activate winter-ptype

test_res_grid="rjpbl_interp_latlon_50km"
model="dynamico"
PS="PS"
U="U1km" 
V="V1km" 

infiles="/glade/u/home/jwillson/dynamical-core/input_files/${test_res_grid}/${model}_files.txt"
detectnodes_out="${test_res_grid}/${model}_detectnodes.txt"
trajectories_file="${test_res_grid}/${model}_trajectories.csv"

DetectNodes --in_data_list $infiles --out $detectnodes_out  --closedcontourcmd "${PS},200.0,5.5,0" --mergedist 6.0 --searchbymin ${PS} --outputcmd "${PS},min,0;_VECMAG(${U},${V}),max,2"

StitchNodes --in_fmt "lon,lat,${PS},wind" --range 8.0 --mintime 10 --maxgap 3 --in $detectnodes_out --out $trajectories_file --out_file_format "csv" --threshold "wind,>=,10.0,10;lat,<=,50.0,10;lat,>=,-50.0,10"