#!/bin/bash -l 

#PBS -N wind_rad_prof
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
trajectories_file="/glade/u/home/jwillson/dynamical-core/trajectories/${test_res_grid}/${model}_trajectories.csv"
radprof_file="${test_res_grid}/${model}.txt"

NodeFileEditor --in_data_list $infiles --in_nodefile $trajectories_file --out_nodefile $radprof_file --out_nodefile_format "csv" --calculate "rprof=radial_wind_profile(${U},${V},159,0.25);rsize=lastwhere(rprof,>,8)" --out_fmt "lon,lat,rsize,rprof"
#--in_fmt "track_id, year, month, day, hour, i, j, lon, lat, PS, wind"