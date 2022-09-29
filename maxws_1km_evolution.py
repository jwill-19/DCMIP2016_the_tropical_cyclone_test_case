import yaml
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from datetime import date
today = date.today()
from utils import open_config, open_dataset
from conversions import hybrid_to_pressure, pressure_to_height

conf = open_config("conf")
test_case = conf['test_case']
grid = conf['grid']
resolution = conf['resolution']

model_conf = open_config("models")
models = list(model_conf.keys())

u_files = open_config("U")
v_files = open_config("V")

fig, ax = plt.subplots(figsize=(12,7), tight_layout=True)
ax.set_title(f"Max 1km Wind Speed Evolution ({resolution})", fontsize=22)
ax.set_xlabel("Days", fontsize=16)
ax.set_ylabel("Max 1km Wind Speed (m/s)", fontsize=16)

for model in models:
    max_ws = []
    u_data = open_dataset(u_files, model)
    v_data = open_dataset(v_files, model)
            
    if model_conf[model]['levels'] == 'height':    
        if model == 'fvm':
            time = np.array([0.25*i for i in range(41)])   
        if model == 'nicam':
            time = u_data.time.values/(60.0*24.0)
        if model.count('csu') == 1:
            time = u_data.time.values
        
        u_interp = u_data.interp(lev=1000.0)
        v_interp = v_data.interp(lev=1000.0)
        for i in range(time.shape[0]):
            max_ws.append(np.max(np.sqrt(np.square(u_interp.U.isel(time=i).values)
                                        +np.square(v_interp.V.isel(time=i).values))))
    else:
        z = pressure_to_height(model)
        if model == 'dynamico':
            time = u_data.time_counter.values/(60.0*60.0*24.0)
        else:
            time = u_data.time.values
        
        if model == 'acme-a':
            u = u_data.u.values
            v = v_data.v.values
        else:
            u = u_data.U.values
            v = v_data.V.values
              
        for i in range(time.shape[0]):
            max_wind = 0.0
            for j in range(u_data.lat.shape[0]):
                for k in range(u_data.lon.shape[0]):
                    u_ijk = u[i,:,j,k]
                    v_ijk = v[i,:,j,k]
                    z_ijk = z[i,:,j,k]
                    u_interp = np.interp(1000.0, z_ijk, u_ijk)
                    v_interp = np.interp(1000.0, z_ijk, v_ijk)
                    res = np.sqrt(np.square(u_interp)+np.square(v_interp))
                    max_wind = max(res, max_wind) 
            max_ws.append(max_wind)

    np.save(f'1km_interpolations/{model}_{today}.npy', max_ws)
    ax.plot(time, max_ws, color=model_conf[model]['color'], label=model)

ax.legend(fontsize=12)
plt.savefig(f"/glade/u/home/jwillson/dynamical-core/figures/msws1km_{test_case}_{grid}_{resolution}.png", dpi=300, bbox_inches='tight')