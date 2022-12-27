import yaml
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from utils import open_config, open_dataset

conf = open_config("conf")
test_case = conf['test_case']
grid = conf['grid']
resolution = conf['resolution']

model_conf = open_config("models")
models = list(model_conf.keys())

precl_files = open_config("PRECL")

fig, ax = plt.subplots(figsize=(12,7), tight_layout=True)
ax.set_title(f"Max Precipitation Rate Evolution ({resolution})", fontsize=22)
ax.set_xlabel("Days", fontsize=16)
ax.set_ylabel("Max Precipitation Rate (m/s)", fontsize=16)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)

for model in models:
    max_precl = []
    try:
        data = open_dataset(precl_files, model)
    except KeyError:   #dynamico doesn't have PRECL data
        continue
    
    if model == 'fvm':
        time = np.array([0.25*i for i in range(41)])
        for i in range(time.shape[0]):
            max_precl.append(np.max(data.PRECT.isel(time=i).values))
    elif model == 'nicam':
        time = data.time.values/(60.0*24.0)
        for i in range(time.shape[0]):
            max_precl.append(np.max(data.PRECL.isel(time=i).values))
    elif model == 'acme-a':
        time = data.time.values
        for i in range(time.shape[0]):
            max_precl.append(np.max(data.precl.isel(time=i).values))
    elif model == 'fv3_dzlow':
        time = data.time.values
        for i in range(time.shape[0]):
            max_precl.append(1.15741e-8*np.max(data.PRECL.isel(time=i).values))
    elif (model.count('csu') == 1) or (model == 'gem'):
        time = data.time.values
        for i in range(time.shape[0]):
            max_precl.append(np.max(data.PRECT.isel(time=i).values))
    else:
        time = data.time.values
        for i in range(time.shape[0]):
            max_precl.append(np.max(data.PRECL.isel(time=i).values))
    
    ax.plot(time, max_precl, color=model_conf[model]['color'], label=model)
        
ax.legend(fontsize=12)
plt.savefig(f"/glade/u/home/jwillson/dynamical-core/figures/{test_case}_{grid}_{resolution}/max_precl_evolution.png", dpi=300, bbox_inches='tight')