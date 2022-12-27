import yaml
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from utils import open_config, open_dataset, get_radprof_arr

conf = open_config("conf")          #get parameters from config file
test_case = conf['test_case']
grid = conf['grid']
resolution = conf['resolution']

model_conf = open_config("models")  #get model names from config file
models = list(model_conf.keys())

fig, ax = plt.subplots(figsize=(12,7), tight_layout=True)
ax.set_title(f"Max Precip Rate Evolution", fontsize=22)
ax.set_xlabel("Days", fontsize=16)
ax.set_ylabel("Precipitation Rate (m/s)", fontsize=16)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)

for model in models:
    #dyamico has no precip information, nicam unable to work on tempestextremes
    if model == 'dynamico' or model == 'nicam': 
        continue
        
    u_files = open_config("U")    #use U since nicam has no time for PRECL variable
    data = open_dataset(u_files, model)   #open example dataset (for time arrays)

    if model == 'dynamico':               #get time array in days
        time = data.time_counter.values/(60.0*60.0*24.0) 
    elif model == 'fvm':
        time = np.array([0.25*i for i in range(41)])
    elif model == 'nicam':
        time = data.time.values/(60.0*24.0)
    else:
        time = data.time.values
    
    #open radial profile file and extract radial profile array
    file = f'/glade/u/home/jwillson/dynamical-core/precip_rad_prof/{test_case}_{grid}_{resolution}/{model}.txt'
    precip_rprof = get_radprof_arr(file)
    
    if model == 'fv3_dzlow':
        precip_rprof = 1.15741e-8*precip_rprof  #convert to m/s 
    
    #create array of max precip rate at every timestep
    max_precl = []
    for i in range(time.shape[0]):
        max_precl.append(np.max(precip_rprof[i,:]))
        
    ax.plot(time, max_precl, color=model_conf[model]['color'], label=model)

ax.legend(fontsize=12)
plt.savefig(f'figures/{test_case}_{grid}_{resolution}/precip_rprof_evolution.png', dpi=300, bbox_inches='tight')