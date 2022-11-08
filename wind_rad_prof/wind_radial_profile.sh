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
models=("acme-a" "cam-se" "csu_CP" "csu_LZ" "dynamico" "fv3_dzlow" "fvm" "gem" "icon" "nicam")
PS=("ps" "PS" "PS" "PS" "PS" "PS" "P(0)" "PS" "PS" "PS")
U=("U1km" "U1km" "U1km" "U1km" "U1km" "U1km" "U1km" "U1km" "U1km" "U1km")
V=("V1km" "V1km" "V1km" "V1km" "V1km" "V1km" "V1km" "V1km" "V1km" "V1km")

for i in {0..9};
do
    infiles="/glade/u/home/jwillson/dynamical-core/input_files/${test_res_grid}/${models[i]}_files.txt"
    trajectories_file="/glade/u/home/jwillson/dynamical-core/trajectories/${test_res_grid}/${models[i]}_trajectories.csv"
    radprof_file="${test_res_grid}/${models[i]}.txt"

    NodeFileEditor --in_data_list $infiles --in_nodefile $trajectories_file --out_nodefile $radprof_file --out_nodefile_format "csv" --calculate "rprof=radial_wind_profile(${U[i]},${V[i]},159,0.25);rsize=lastwhere(rprof,>,8)" --out_fmt "lon,lat,rsize,rprof"
done
#--in_fmt "track_id,year,month,day,hour,i,j,lon,lat,ps,wind"