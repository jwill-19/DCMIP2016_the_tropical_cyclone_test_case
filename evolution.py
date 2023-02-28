import yaml
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from utils import open_config, open_dataset, get_radprof_arr, get_plot_name

conf = open_config("conf")                   #get parameters from config file
test_case = conf['test_case']
grid = conf['grid']
resolution = conf['resolution']
height = conf['height']

model_conf = open_config("models")           #open model config file

if resolution == "25km":                     #get model names from config file
    models = []
    for model in list(model_conf.keys()):        
        if model_conf[model]['25km'] == True:
            models.append(model)
else:
    models = list(model_conf.keys())

u_files = open_config("U")                   #open relevant datasets
ps_files = open_config("PS")

fig, ax = plt.subplots(2, 1, sharex=True, figsize=(12,12), tight_layout=True)

for ax, i in zip(ax.ravel(), range(2)):
    for model in models:
        if i == 0:
            data = open_dataset(ps_files, model) #open example dataset (for time arrays) and trajectory file
            file = f'/glade/u/home/jwillson/dynamical-core/trajectories/{test_case}_{grid}_{resolution}/{model}_trajectories.csv'
            ps_data = pd.read_csv(file)
            ps = ps_data[ps_data.columns[-2]]    #pressure is the second to last column

            if model == 'dynamico':              #get time array in days 
                time = data.time_counter.values/(60.0*60.0*24.0) 
            elif model == 'fvm':
                time = np.array([0.25*i for i in range(41)])
            elif model == 'nicam':
                time = data.time.values/(60.0*24.0)
            else:
                time = data.time.values

            if resolution == "25km":
                ps = ps[:41]                     #only keep the first track in some 25km models
            ax.plot(time, ps/100, color=model_conf[model]['color'], label=get_plot_name(model))
        else:
            data = open_dataset(u_files, model)   #open example dataset (for time arrays)
    
            if model == 'dynamico':               #get time array in days
                time = data.time_counter.values/(60.0*60.0*24.0) 
            elif model == 'fvm':
                time = np.array([0.25*i for i in range(41)])
            elif model == 'nicam':
                time = data.time.values/(60.0*24.0)
            else:
                time = data.time.values

            file = f'/glade/u/home/jwillson/dynamical-core/wind_rad_prof/{test_case}_{grid}_{resolution}/{model}_{height}.txt'  
            rprof = get_radprof_arr(file) #extract radial profile from text file
            max_wind = []

            for i in range(time.shape[0]):  #calculate max wind at each timestep
                max_wind.append(np.max(rprof[i,:]))

            if resolution == "25km":
                max_wind = max_wind[:41]        #only keep the first track in some 25km models
            ax.plot(time, max_wind, color=model_conf[model]['color'], label=get_plot_name(model))
        
    if i == 0:                                   #set labels and fontsizes
        ax.set_ylabel("Pressure (hPa)", fontsize=22)
    else:
        ax.set_xlabel("Days", fontsize=22)
        ax.set_ylabel("Wind Speed (m/s)", fontsize=22)
        
    ax.tick_params(axis='x', labelsize=16)
    ax.tick_params(axis='y', labelsize=16)

handles = []  #add custom legend
for model in models:
    handles.append(mpatches.Patch(color=model_conf[model]['color'], label=get_plot_name(model)))
ax.legend(handles=handles, bbox_to_anchor=(0.935, -0.15), ncol=5, fontsize=16)
plt.savefig(f"figures/{test_case}_{grid}_{resolution}/evolution_combined.png", dpi=300, bbox_inches='tight')