import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from utils import open_config, open_dataset, get_plot_name

conf = open_config("conf")             #get parameters from config file
test_case = conf['test_case']                   
grid = conf['grid']
resolution = conf['resolution'] 

model_conf = open_config('models')     #get list of models
models = list(model_conf.keys())

models.pop(models.index('dynamico'))   #no information for dynamico and nicam, gem failed in tempestextremes
models.pop(models.index('nicam'))
models.pop(models.index('gem'))

fig, ax = plt.subplots(2, 1, sharex=True, figsize=(11,12), tight_layout=True)

for ax, i in zip(ax.ravel(), range(2)):
    for model in models:
        #dyamico has no precip information, nicam and gem unable to work on tempestextremes
        if model == 'dynamico' or model == 'nicam' or model == 'gem': 
            continue
            
        #open composite file and extract snapshot array
        file = f"/glade/u/home/jwillson/dynamical-core/precip_composite/rjpbl_interp_latlon_50km/{model}_composite_snap.nc"
        data = xr.open_dataset(file, decode_times=False)
        precl = data.snap_PRECL.values
    
        if model == 'fv3_dzlow':
            precl = 1.15741e-8*precl  #convert to m/s
    
        if model == 'dynamico':                           #dynamico is 3 hourly
            time = data.time_counter.values/(60.0*60.0*24.0) 
        else:
            time = np.array([0.25*j for j in range(41)])  #standard DCMIP2016 time values
        
        if i == 0: #plot max or avg precl depending on if its the first or second iteration
            #create array of max precip rate at every timestep
            max_precl = []
            for k in range(time.shape[0]):
                max_precl.append(np.max(precl[k,:,:]))
            
            ax.plot(time, max_precl, color=model_conf[model]['color'], label=get_plot_name(model))
        else:
            #create array of avg precip rate at every timestep
            avg_precl = []
            for k in range(time.shape[0]):
                avg_precl.append(np.mean(precl[k,:,:]))
                
            ax.plot(time, avg_precl, color=model_conf[model]['color'], label=get_plot_name(model))
        
    if i == 0:           #set labels and fontsizes
        ax.set_ylabel("Max Precipitation Rate (m/s)", fontsize=22)
    else:
        ax.set_xlabel("Days", fontsize=22)
        ax.set_ylabel("Avg Precipitation Rate (m/s)", fontsize=22)
        
    ax.tick_params(axis='x', labelsize=16)
    ax.tick_params(axis='y', labelsize=16)

handles = []             #add custom legend
for model in models:
    handles.append(mpatches.Patch(color=model_conf[model]['color'], label=get_plot_name(model)))
ax.legend(handles=handles, bbox_to_anchor=(0.84, -0.15), ncol=4, fontsize=16)
plt.savefig(f"/glade/u/home/jwillson/dynamical-core/figures/{test_case}_{grid}_{resolution}/precl_evolution.png", 
            dpi=300, bbox_inches='tight')