import yaml
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from utils import open_config

test_case = "rjpbl"
grid = "interp_latlon"
resolution = "50km"

config = "/glade/u/home/jwillson/dynamical-core/PS.yml"
ps_files = open_config(config)
models = list(ps_files[f"{test_case}"][f"{grid}"][f"{resolution}"].keys())
colors = ps_files["colors"]

fig, ax = plt.subplots(figsize=(12,7), tight_layout=True)
ax.set_title(f"Min Surface Pressure Evolution ({resolution})", fontsize=22)
ax.set_xlabel("Days", fontsize=16)
ax.set_ylabel("Min Surface Pressure (Pa)", fontsize=16)

for model in models:
    min_ps = []
    file = ps_files["data_path"] + ps_files[f"{test_case}"][f"{grid}"][f"{resolution}"][model]
    data = xr.open_dataset(file, decode_times=False)
    
    if model == 'dynamico':
        time = data.time_instant.values/(60.0*60.0*24.0)
        for i in range(time.shape[0]):
            min_ps.append(np.min(data.PS.isel(time_counter=i).values))
    elif model == 'fvm':
        time = np.array([0.25*i for i in range(41)])
        for i in range(time.shape[0]):
            min_ps.append(np.min(data.P.isel(lev=0, time=i).values))
    elif model == 'nicam':
        time = data.time.values/(60.0*24.0)
        for i in range(time.shape[0]):
            min_ps.append(np.min(data.PS.isel(time=i).values))
    elif model == 'acme-a':
        time = data.time.values
        for i in range(time.shape[0]):
            min_ps.append(np.min(data.ps.isel(time=i).values))
    else:
        time = data.time.values
        for i in range(time.shape[0]):
            min_ps.append(np.min(data.PS.isel(time=i).values))
    
    ax.plot(time, min_ps, color=colors[model], label=model)
        
ax.legend(fontsize=12)
plt.savefig(f"/glade/u/home/jwillson/dynamical-core/figures/ps_{test_case}_{grid}_{resolution}.png", dpi=300, bbox_inches='tight')