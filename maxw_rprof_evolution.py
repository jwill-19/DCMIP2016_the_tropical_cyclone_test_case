import yaml
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
from utils import open_config, open_dataset, get_radprof_arr

conf = open_config("conf")   #get parameters from config file
test_case = conf['test_case']
grid = conf['grid']
resolution = conf['resolution']
height = conf['height']

model_conf = open_config("models") #get model names from config file
models = list(model_conf.keys())

u_files = open_config("U")

fig, ax = plt.subplots(figsize=(12,7), tight_layout=True)
ax.set_title(f"Max {height}m Wind Speed Evolution", fontsize=22)
ax.set_xlabel("Days", fontsize=16)
ax.set_ylabel("Max 1km Wind Speed (m/s)", fontsize=16)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)

for model in models:
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
    
    ax.plot(time, max_wind, color=model_conf[model]['color'], label=model)
        
ax.legend(fontsize=12)
plt.savefig(f"/glade/u/home/jwillson/dynamical-core/figures/{test_case}_{grid}_{resolution}/maxw1km_rprof_evolution_{height}.png",
            dpi=300, bbox_inches='tight')