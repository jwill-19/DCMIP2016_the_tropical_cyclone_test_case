import yaml
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
from utils import open_config, open_dataset, get_radprof_arr

conf = open_config("conf")
test_case = conf['test_case']
grid = conf['grid']
resolution = conf['resolution']

model_conf = open_config("models")
models = list(model_conf.keys())

fig, ax = plt.subplots(figsize=(12,7), tight_layout=True)
dist = [i*0.25*111.321 for i in range(159)]  #calculate distance based on bin size and total bins,
                                             #convert to distance from degrees
for model in models:                         #calculate the time averaged 1km wind radial profile
    rprof = get_radprof_arr(f"wind_rad_prof/{test_case}_{grid}_{resolution}/{model}.txt")
    rprof = np.mean(rprof, axis=0)
    ax.plot(dist, rprof, color=model_conf[model]['color'], label=model)
    
ax.set_title(f"Time Averaged Radial 1km Wind Profile", fontsize=22)
ax.set_xlabel(f'Distance from center (km)', fontsize=16)
ax.set_ylabel(f'Wind Speed (m/s)', fontsize=16)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)
ax.legend(fontsize=12)
ax.set_xlim([0,1000])
plt.savefig(f'figures/{test_case}_{grid}_{resolution}/wrprof_all_times_avg.png', dpi=300, bbox_inches='tight')