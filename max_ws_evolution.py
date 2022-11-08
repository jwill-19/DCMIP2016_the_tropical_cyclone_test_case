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

u_files = open_config("U")
v_files = open_config("V")

fig, ax = plt.subplots(figsize=(12,7), tight_layout=True)
ax.set_title(f"Max Surface Wind Speed Evolution ({resolution})", fontsize=22)
ax.set_xlabel("Days", fontsize=16)
ax.set_ylabel("Max Surface Wind Speed (m/s)", fontsize=16)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)

for model in models:
    max_ws = []
    u_data = open_dataset(u_files, model)
    v_data = open_dataset(v_files, model)
    
    if model == 'dynamico':
        time = u_data.time_counter.values/(60.0*60.0*24.0)
        for i in range(time.shape[0]):
            max_ws.append(np.max(np.sqrt(np.square(u_data.U.isel(lev=0, time_counter=i).values)
                                         +np.square(v_data.V.isel(lev=0, time_counter=i).values))))
    elif model == 'fvm':
        time = np.array([0.25*i for i in range(41)])
        for i in range(time.shape[0]):
            max_ws.append(np.max(np.sqrt(np.square(u_data.U.isel(lev=0, time=i).values)
                                         +np.square(v_data.V.isel(lev=0, time=i).values))))
    elif model == 'nicam':
        time = u_data.time.values/(60.0*24.0)
        for i in range(time.shape[0]):
            max_ws.append(np.max(np.sqrt(np.square(u_data.U.isel(lev=0, time=i).values)
                                         +np.square(v_data.V.isel(lev=0, time=i).values))))
    elif model == 'acme-a':
        time = u_data.time.values
        for i in range(time.shape[0]):
            max_ws.append(np.max(np.sqrt(np.square(u_data.u.isel(lev=29, time=i).values)
                                         +np.square(v_data.v.isel(lev=29, time=i).values))))       
    elif model.count('csu') == 1:
        time = u_data.time.values
        for i in range(time.shape[0]):
            max_ws.append(np.max(np.sqrt(np.square(u_data.U.isel(lev=0, time=i).values)
                                         +np.square(v_data.V.isel(lev=0, time=i).values))))
    elif model == 'fv3_dzlow':
        time = u_data.time.values
        for i in range(time.shape[0]):
            max_ws.append(np.max(np.sqrt(np.square(u_data.U.isel(pfull=29, time=i).values)
                                         +np.square(v_data.V.isel(pfull=29, time=i).values))))       
    elif model == 'gem':
        time = u_data.time.values
        for i in range(time.shape[0]):
            max_ws.append(np.max(np.sqrt(np.square(u_data.U.isel(ilev=29, time=i).values)
                                         +np.square(v_data.V.isel(ilev=29, time=i).values))))
    else:
        time = u_data.time.values
        for i in range(time.shape[0]):
            max_ws.append(np.max(np.sqrt(np.square(u_data.U.isel(lev=29, time=i).values)
                                         +np.square(v_data.V.isel(lev=29, time=i).values))))
    
    ax.plot(time, max_ws, color=model_conf[model]['color'], label=model)

ax.legend(fontsize=12)
plt.savefig(f"/glade/u/home/jwillson/dynamical-core/figures/{test_case}_{grid}_{resolution}/msws_evolution.png", dpi=300, bbox_inches='tight')