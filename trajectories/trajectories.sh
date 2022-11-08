#!/bin/bash -l 

#PBS -N trajectories
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
#U=("u(29)" "U(29)" "U(0)" "U(0)" "U(0)" "U(29)" "U(0)" "U(29)" "U(29)" "U(0)")
#V=("v(29)" "V(29)" "V(0)" "V(0)" "V(0)" "V(29)" "V(0)" "V(29)" "V(29)" "V(0)")
U=("U1km" "U1km" "U1km" "U1km" "U1km" "U1km" "U1km" "U1km" "U1km" "U1km")
V=("V1km" "V1km" "V1km" "V1km" "V1km" "V1km" "V1km" "V1km" "V1km" "V1km")

for i in {0..9};
do
    infiles="/glade/u/home/jwillson/dynamical-core/input_files/${test_res_grid}/${models[i]}_files.txt"
    detectnodes_out="${test_res_grid}/${models[i]}_detectnodes.txt"
    trajectories_file="${test_res_grid}/${models[i]}_trajectories.csv"

    DetectNodes --in_data_list $infiles --out $detectnodes_out  --closedcontourcmd "${PS[i]},200.0,5.5,0" --mergedist 6.0 --searchbymin ${PS[i]} --outputcmd "${PS[i]},min,0;_VECMAG(${U[i]},${V[i]}),max,2"

    StitchNodes --in_fmt "lon,lat,${PS[i]},wind" --range 8.0 --mintime 10 --maxgap 3 --in $detectnodes_out --out $trajectories_file --out_file_format "csv" --threshold "wind,>=,10.0,10;lat,<=,50.0,10;lat,>=,-50.0,10"
done