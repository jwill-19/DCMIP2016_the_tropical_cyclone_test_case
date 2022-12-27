import yaml
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from utils import open_config, open_dataset, get_radprof_arr

conf = open_config("conf")                   #get parameters from config file
test_case = conf['test_case']                   
grid = conf['grid']
resolution = conf['resolution'] 
day = conf['day']                            #begin time average after this day
height_names = conf['height_names']          #names and values of height levels used
height_vals = np.array(conf['height_vals'])

model_conf = open_config("models")           #get model names from config file
models = list(model_conf.keys())

dist = np.array([i*0.25*111.321 for i in range(159)])     #distance array based on TempestExtremes settings
time = np.array([0.25*i for i in range(41)])
idx = np.argwhere(time == day)[0,0]           #only include times after day 4

composites = []               #create composites for every model
for model in models:
    rprofs = []
    for height in height_names:
        rprof = get_radprof_arr(f"wind_rad_prof/{test_case}_{grid}_{resolution}/{model}_{height}.txt")
        rprof = rprof[idx:,:]  #average over certain times in the simulation
        rprof = np.mean(rprof, axis=0)
        rprofs.append(rprof)   #append radial profile to composite
    
    rprofs = np.array(rprofs)
    composites.append(rprofs)

composites = np.array(composites)  #find max value for normalization
max_val = np.max(composites)

fig, ax = plt.subplots(5, 2, sharex=True, sharey=True, figsize=(10,15), constrained_layout=True)
cmap = plt.cm.turbo                                   #colormap       
norm = mpl.colors.Normalize(vmin=0, vmax=max_val)     #normalize based on max value in all models
cax = ax.ravel().tolist()                             #colorbar axes (list of all axes)

for ax, composite, model in zip(ax.ravel(), composites, models):  #plot the composites
    ax.set_title(model, fontsize=20)
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    ax.set_xlim([0,500])
    ax.contourf(dist, height_vals/1000, composite, levels=2*len(height_vals), norm=norm, cmap=cmap)

# plot the colorbar
fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=cax, shrink=0.75, location='bottom')
    
fig.add_subplot(111, frameon=False)    #create new axes for axis labels
plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
plt.text(0.4, 0.05, "Radius (km)", fontsize=18)
plt.ylabel("Height (km)", fontsize=18)
plt.savefig(f'figures/{test_case}_{grid}_{resolution}/windcomposite_{day}to10_avg.png', dpi=300, bbox_inches='tight')