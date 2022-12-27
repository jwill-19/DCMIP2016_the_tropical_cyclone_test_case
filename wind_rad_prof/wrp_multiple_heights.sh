#!/bin/bash -l 

#PBS -N wind_rad_prof
#PBS -A NAML0001
#PBS -l walltime=12:00:00
#PBS -l select=1:ncpus=4:ngpus=0:mem=64GB
#PBS -q casper
#PBS -j oe

module load nco
source ~/.bashrc
conda activate winter-ptype

test_res_grid="rjpbl_interp_latlon_50km"
#models=("acme-a" "cam-se" "csu_CP" "csu_LZ" "dynamico" "fv3_dzlow" "fvm" "gem" "icon" "nicam") #len=10
models=("dynamico" "fv3_dzlow")
heights=("100" "150" "200" "250" "500" "1000" "1500" "2000" "3000" "4000" "5000" "6000" "7000" "8000" "9000" "10000" "11000" "12000" "13000" "14000" "15000" "16000") #len=22

for i in {0..1};
do
    infiles="/glade/u/home/jwillson/dynamical-core/input_files/${test_res_grid}/${models[i]}_files.txt"
    trajectories_file="/glade/u/home/jwillson/dynamical-core/trajectories/${test_res_grid}/${models[i]}_trajectories.csv"
    for j in {0..21};
    do
        radprof_file="${test_res_grid}/${models[i]}_${heights[j]}.txt"
        NodeFileEditor --in_data_list $infiles --in_nodefile $trajectories_file --out_nodefile $radprof_file --out_nodefile_format "csv" --calculate "rprof=radial_wind_profile(U${heights[j]},V${heights[j]},159,0.25);rsize=lastwhere(rprof,>,8)" --out_fmt "lon,lat,rsize,rprof"
    done
done