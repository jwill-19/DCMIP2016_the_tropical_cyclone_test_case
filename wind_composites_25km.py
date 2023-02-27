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

model_conf = open_config("models")           #open model config file
models = []

for model in list(model_conf.keys()):        #get model names from config file
    if model_conf[model]['25km'] == True:
        models.append(model)
    
dist = np.array([i*0.25*111.321 for i in range(159)])     #distance array based on TempestExtremes settings
time = np.array([0.25*i for i in range(41)])
start_idx = np.argwhere(time == day)[0,0]           #only include times after day 4
end_idx = 41                                        #only include up to day 10

composites = []               #create composites for every model
for model in models:
    rprofs = []
    for height in height_names:
        rprof = get_radprof_arr(f"wind_rad_prof/{test_case}_{grid}_{resolution}/{model}_{height}.txt")
        rprof = rprof[start_idx:end_idx,:]  #average over certain times in the simulation
        rprof = np.mean(rprof, axis=0)
        rprofs.append(rprof)   #append radial profile to composite

    rprofs = np.array(rprofs)
    composites.append(rprofs)
        
composites = np.array(composites)  #find max value for normalization
max_val = np.max(composites)

fig, ax = plt.subplots(5, 1, sharex=True, sharey=True, figsize=(6,9), constrained_layout=True)
cmap = plt.cm.turbo                                   #colormap       
norm = mpl.colors.Normalize(vmin=0, vmax=max_val)     #normalize based on max value in all models
cax = ax.ravel().tolist()                             #colorbar axes (list of all axes)

for ax, composite, model in zip(ax.ravel(), composites, models):  #plot the composites
    ax.set_title(model, fontsize=16)
    if model == 'fvm':
        ax.tick_params(labelcolor='none', which='both', left=False)
    else:
        ax.tick_params(axis='x', labelsize=10)
        ax.tick_params(axis='y', labelsize=10)
    ax.set_xlim([0,500])
    ax.contourf(dist, height_vals/1000, composite, levels=2*len(height_vals), norm=norm, cmap=cmap)

# plot the colorbar
fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=cax, shrink=0.75, location='bottom')
    
fig.add_subplot(111, frameon=False)    #create new axes for axis labels
plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
plt.text(0.4, 0.05, "Radius (km)", fontsize=14)
plt.text(-0.2, 0.5, "Height (km)", fontsize=14, rotation='vertical')
plt.savefig(f'figures/{test_case}_{grid}_{resolution}/windcomposite_{day}to10_avg.png', dpi=300, bbox_inches='tight')