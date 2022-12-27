import yaml
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
from utils import open_config, open_dataset

conf = open_config("conf")
test_case = conf['test_case']
grid = conf['grid']
resolution = conf['resolution']

model_conf = open_config("models")
models = list(model_conf.keys())

ps_files = open_config("PS")

fig, ax = plt.subplots(figsize=(12,7), tight_layout=True)
ax.set_title(f"Surface Pressure Evolution at TC Center ({resolution})", fontsize=22)
ax.set_xlabel("Days", fontsize=16)
ax.set_ylabel("Surface Pressure (Pa)", fontsize=16)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)

for model in models:
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
    
    ax.plot(time, ps, color=model_conf[model]['color'], label=model)
        
ax.legend(fontsize=12)
plt.savefig(f"/glade/u/home/jwillson/dynamical-core/figures/{test_case}_{grid}_{resolution}/ps_center_evolution.png",
            dpi=300, bbox_inches='tight')