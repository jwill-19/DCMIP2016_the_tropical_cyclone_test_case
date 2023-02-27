import numpy as np
import xarray as xr
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from utils import open_config, open_dataset, get_plot_name, get_radprof_arr

conf = open_config("conf")             #get parameters from config file
test_case = conf['test_case']                   
grid = conf['grid']
resolution = conf['resolution'] 
day = conf['day']                      #begin time average after this day
height = conf['height']                #height of rprof to be plotted

model_conf = open_config('models')     #get list of models
models = list(model_conf.keys())

fig, ax = plt.subplots(2, 1, sharex=True, figsize=(11,12), tight_layout=True)

for ax, i in zip(ax.ravel(), range(2)):
    for model in models:
        dist = [i*0.25*111.321 for i in range(159)]  #calculate distance based on bin size and total bins, convert to distance from degrees
        time = np.array([0.25*i for i in range(41)]) #create time array in days
        start_idx = np.argwhere(time == day)[0,0]    #calculate index of specified start day
        end_idx = 41                                 #end at day 10   
        
        if i == 0:  #plot pressure radial profiles
            rprof = get_radprof_arr(f"ps_rad_prof/{test_case}_{grid}_{resolution}/{model}.txt")
            rprof = rprof[start_idx:end_idx,:]
            rprof = np.mean(rprof, axis=0)
            ax.plot(dist, rprof/100, color=model_conf[model]['color'], label=get_plot_name(model))
        else:       #plot wind radial profiles
            rprof = get_radprof_arr(f"wind_rad_prof/{test_case}_{grid}_{resolution}/{model}_{height}.txt")
            rprof = rprof[start_idx:end_idx,:]
            rprof = np.mean(rprof, axis=0)
            ax.plot(dist, rprof, color=model_conf[model]['color'], label=get_plot_name(model))
        
        
    if i == 0:           #set labels, fontsizes, and x/y limits
        ax.set_ylabel("Pressure (hPa)", fontsize=22)
        ax.set_ylim([900,1025])
    else:
        ax.set_xlabel("Distance from center (km)", fontsize=22)
        ax.set_ylabel("Wind Speed (m/s)", fontsize=22)
        
    ax.set_xlim([0,1000])
    ax.tick_params(axis='x', labelsize=16)
    ax.tick_params(axis='y', labelsize=16)

handles = []             #add custom legend
for model in models:
    handles.append(mpatches.Patch(color=model_conf[model]['color'], label=get_plot_name(model)))
ax.legend(handles=handles, bbox_to_anchor=(0.995, -0.15), ncol=5, fontsize=16)
plt.savefig(f"/glade/u/home/jwillson/dynamical-core/figures/{test_case}_{grid}_{resolution}/windps_rprofs.png", 
            dpi=300, bbox_inches='tight')