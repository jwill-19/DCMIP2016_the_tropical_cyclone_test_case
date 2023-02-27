import yaml
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
from utils import open_config, open_dataset, get_radprof_arr, get_plot_name

conf = open_config("conf")                   #get parameters from config file
test_case = conf['test_case']                   
grid = conf['grid']
resolution = conf['resolution'] 
day = conf['day']                            #begin time average after this day
height = conf['height']                      #height of rprof to be plotted

model_conf = open_config("models")           #open model config file

if resolution == "25km":                     #get model names from config file
    models = []
    for model in list(model_conf.keys()):        
        if model_conf[model]['25km'] == True:
            models.append(model)
else:
    models = list(model_conf.keys())

fig, ax = plt.subplots(figsize=(12,7), tight_layout=True)
dist = [i*0.25*111.321 for i in range(159)]  #calculate distance based on bin size and total bins, convert to distance from degrees
time = np.array([0.25*i for i in range(41)]) #create time array in days
start_idx = np.argwhere(time == day)[0,0]    #calculate index of specified start day
end_idx = 41                                 #end at day 10   

for model in models:                         #loop through models and plot wind radial profiles
    rprof = get_radprof_arr(f"wind_rad_prof/{test_case}_{grid}_{resolution}/{model}_{height}.txt")
    rprof = rprof[start_idx:end_idx,:]
    rprof = np.mean(rprof, axis=0)
    ax.plot(dist, rprof, color=model_conf[model]['color'], label=get_plot_name(model))
    
# ax.set_title(f"Wind Radial Profile {height}m", fontsize=22)
ax.set_xlabel(f'Distance from center (km)', fontsize=22)
ax.set_ylabel(f'Wind Speed (m/s)', fontsize=22)
ax.tick_params(axis='x', labelsize=16)
ax.tick_params(axis='y', labelsize=16)
ax.legend(fontsize=16)
ax.set_xlim([0,1000])
plt.savefig(f'figures/{test_case}_{grid}_{resolution}/wrprof_{day}to10avg_{height}m.png', dpi=300, bbox_inches='tight')