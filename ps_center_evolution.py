import yaml
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
from utils import open_config, open_dataset, get_plot_name

conf = open_config("conf")                   #get parameters from config file
test_case = conf['test_case']
grid = conf['grid']
resolution = conf['resolution']

model_conf = open_config("models")           #open model config file

if resolution == "25km":                     #get model names from config file
    models = []
    for model in list(model_conf.keys()):        
        if model_conf[model]['25km'] == True:
            models.append(model)
else:
    models = list(model_conf.keys())

ps_files = open_config("PS")

fig, ax = plt.subplots(figsize=(12,7), tight_layout=True)
ax.set_title(f"Minimum Surface Pressure Evolution", fontsize=22)
ax.set_xlabel("Days", fontsize=16)
ax.set_ylabel("Surface Pressure (Pa)", fontsize=16)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)

for model in models:                     #loop through all models
    data = open_dataset(ps_files, model) #open example dataset (for time arrays) and trajectory file
    file = f'/glade/u/home/jwillson/dynamical-core/trajectories/{test_case}_{grid}_{resolution}/{model}_trajectories.csv'
    ps_data = pd.read_csv(file)
    ps = ps_data[ps_data.columns[-2]]   #pressure is the second to last column
    
    if model == 'dynamico':             #get time array in days 
        time = data.time_counter.values/(60.0*60.0*24.0) 
    elif model == 'fvm':
        time = np.array([0.25*i for i in range(41)])
    elif model == 'nicam':
        time = data.time.values/(60.0*24.0)
    else:
        time = data.time.values
    
    if resolution == "25km":
        ps = ps[:41]                        #only keep the first track in some 25km models
    ax.plot(time, ps, color=model_conf[model]['color'], label=get_plot_name(model))
        
ax.legend(fontsize=12)
plt.savefig(f"/glade/u/home/jwillson/dynamical-core/figures/{test_case}_{grid}_{resolution}/ps_center_evolution.png",
            dpi=300, bbox_inches='tight')