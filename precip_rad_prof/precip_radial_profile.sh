#!/bin/bash -l 

#PBS -N precip_rad_prof
#PBS -A NAML0001
#PBS -l walltime=12:00:00
#PBS -l select=1:ncpus=1:ngpus=0:mem=32GB
#PBS -q casper
#PBS -j oe

source ~/.bashrc
conda activate winter-ptype

test_res_grid="rjpbl_interp_latlon_50km"
models=("acme-a" "cam-se" "csu_CP" "csu_LZ" "fv3_dzlow" "fvm" "gem" "icon" "nicam")
U="U1km"
V="V1km"
PRECL=("precl" "PRECL" "PRECT" "PRECT" "PRECL" "PRECT" "PRECT" "PRECL" "PRECL")

for i in {0..8};
do
    infiles="/glade/u/home/jwillson/dynamical-core/input_files/${test_res_grid}/${models[i]}_files.txt"
    trajectories_file="/glade/u/home/jwillson/dynamical-core/trajectories/${test_res_grid}/${models[i]}_trajectories.csv"
    radprof_file="${test_res_grid}/${models[i]}.txt"

    NodeFileEditor --in_data_list $infiles --in_nodefile $trajectories_file --out_nodefile $radprof_file --out_nodefile_format "csv" --calculate "precip_prof=radial_profile(${PRECL[i]},159,0.25);rsize=lastwhere(precip_prof,>,0)" --out_fmt "lon,lat,rsize,precip_prof"
done