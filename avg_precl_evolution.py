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
ax.set_title(f"Area Averaged Precipitation Rate ({resolution})", fontsize=22)
ax.set_xlabel("Days", fontsize=16)
ax.set_ylabel("Precipitation Rate (m/s)", fontsize=16)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)

for model in models:
    avg_precl = []
    try:
        data = open_dataset(precl_files, model)
    except KeyError:
        continue
    
    if model == 'fvm':
        time = np.array([0.25*i for i in range(41)])
    elif model == 'nicam':
        time = data.time.values/(60.0*24.0)
    else:
        time = data.time.values
        
    if (model.count('csu') == 1) or (model == 'gem') or (model == 'fvm'):
        precl = data.PRECT.values
    elif model == 'acme-a':
        precl = data.precl.values
    else:
        precl = data.PRECL.values
        
    for i in range(time.shape[0]):
        precl_i = precl[i,:,:].reshape(data.lat.shape[0]*data.lon.shape[0])
        precl_i = precl_i[precl_i > 0]
        if precl_i.shape[0] == 0:
            area_avg = 0
        else:
            area_avg = np.mean(precl_i)
        
        if model == 'fv3_dzlow':
            avg_precl.append(1.15741e-8*area_avg)
        else:
            avg_precl.append(area_avg)
    
    ax.plot(time, avg_precl, color=model_conf[model]['color'], label=model)
        
ax.legend(fontsize=12)
plt.savefig(f"/glade/u/home/jwillson/dynamical-core/figures/{test_case}_{grid}_{resolution}/avg_precl_evolution.png", dpi=300, bbox_inches='tight')