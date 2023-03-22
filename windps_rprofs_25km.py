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
res50 = '50km'                         #original resolution
day = conf['day']                      #begin time average after this day
height = conf['height']                #height of rprof to be plotted

model_conf = open_config('models')     #get list of models
models = []

for model in list(model_conf.keys()):  #get model names from config file
    if model_conf[model]['25km'] == True:
        models.append(model)
        
conf = open_config("conf")             #get parameters from config file
test_case = conf['test_case']                   
grid = conf['grid']
resolution = conf['resolution']
res50 = '50km'                         #original resolution
day = conf['day']                      #begin time average after this day
height = conf['height']                #height of rprof to be plotted

model_conf = open_config('models')     #get list of models
models = []

for model in list(model_conf.keys()):  #get model names from config file
    if model_conf[model]['25km'] == True:
        models.append(model)
        
fig, ax = plt.subplots(2, 1, sharex=True, figsize=(11,12), tight_layout=True)

dist = [i*0.25*111.321 for i in range(159)]
midpoints = [(dist[i]+dist[i+1])/2.0 for i in range(158)]  #calculate distance based on bin size and total bins
                                                           #and convert to distance from degrees
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
            ax.plot(midpoints, (rprof/100)[1:], color=model_conf[model]['color'])
            
            #now use same procedure to plot the original 50km curves on the same plot
            rprof = get_radprof_arr(f"ps_rad_prof/{test_case}_{grid}_{res50}/{model}.txt")
            rprof = rprof[start_idx:end_idx,:]
            rprof = np.mean(rprof, axis=0)
            ax.plot(midpoints, (rprof/100)[1:], linestyle='dashed', alpha=0.5, color=model_conf[model]['color'])
        else:       #plot wind radial profiles
            rprof = get_radprof_arr(f"wind_rad_prof/{test_case}_{grid}_{resolution}/{model}_{height}.txt")
            rprof = rprof[start_idx:end_idx,:]
            rprof = np.mean(rprof, axis=0)
            ax.plot(midpoints, rprof[1:], color=model_conf[model]['color'])
            
            #now use same procedure to plot the original 50km curves on the same plot
            rprof = get_radprof_arr(f"wind_rad_prof/{test_case}_{grid}_{res50}/{model}_{height}.txt")
            rprof = rprof[start_idx:end_idx,:]
            rprof = np.mean(rprof, axis=0)
            ax.plot(midpoints, rprof[1:], linestyle='dashed', alpha=0.5, color=model_conf[model]['color'])
            
    if i == 0:           #set labels and fontsizes
        ax.set_ylabel("Pressure (hPa)", fontsize=22)
    else:
        ax.set_xlabel("Distance from center (km)", fontsize=22)
        ax.set_ylabel("Wind Speed (m/s)", fontsize=22)
        
    ax.set_xlim([0,1000])
    ax.tick_params(axis='x', labelsize=16)
    ax.tick_params(axis='y', labelsize=16)

handles = []             #add custom legend
for model in models:
    handles.append(mpatches.Patch(color=model_conf[model]['color'], label=get_plot_name(model)))
ax.legend(handles=handles, bbox_to_anchor=(0.95, -0.15), ncol=5, fontsize=16)
plt.savefig(f"figures/{test_case}_{grid}_{resolution}/wprprofs_{day}to10avg_{height}m.png", dpi=300, bbox_inches='tight')