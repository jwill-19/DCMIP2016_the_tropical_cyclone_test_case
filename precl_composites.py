import numpy as np
import xarray as xr
import matplotlib as mpl
import matplotlib.pyplot as plt
from utils import open_config, open_dataset, get_plot_name

conf = open_config("conf")             #get parameters from config file
test_case = conf['test_case']                   
grid = conf['grid']
resolution = conf['resolution'] 

model_conf = open_config('models')     #get list of models
models = list(model_conf.keys())

models.pop(models.index('dynamico'))   #no information for dynamico and nicam failed in tempestextremes
models.pop(models.index('nicam'))

max_val = 0.0
for model in models:  #calculate max value in all composites
    #open composite file and extract composite array 
    file = f"/glade/u/home/jwillson/dynamical-core/precip_composite/rjpbl_interp_latlon_50km/{model}_composite.nc"
    data = xr.open_dataset(file, decode_times=False)
    precl = data.PRECL.values
    
    if model == 'fv3_dzlow':
        precl = 1.15741e-8*precl  #convert to m/s
    
    val = np.max(precl)
    max_val = max(max_val, val)

fig, ax = plt.subplots(4, 2, sharex=True, sharey=True, figsize=(10,15), constrained_layout=True)
cmap = plt.cm.turbo                                   #colormap       
norm = mpl.colors.Normalize(vmin=0, vmax=max_val)     #normalize based on max value in all models
cax = ax.ravel().tolist()                             #colorbar axes (list of all axes)

for ax, model in zip(ax.ravel(), models): 
    #open composite file and extract composite array 
    file = f"/glade/u/home/jwillson/dynamical-core/precip_composite/rjpbl_interp_latlon_50km/{model}_composite.nc"
    data = xr.open_dataset(file, decode_times=False)
    precl = data.PRECL.values
    
    if model == 'fv3_dzlow':
        precl = 1.15741e-8*precl  #convert to m/s
    
    ax.set_title(get_plot_name(model), fontsize=22) #set plot parameters
    ax.tick_params(axis='x', labelsize=16)
    ax.tick_params(axis='y', labelsize=16)
    if model == 'fv3_dzlow':
        ax.set_ylabel("y (GCD)", loc='top', fontsize=22)
    ax.contourf(data.x.values, data.y.values, precl, levels=2*len(data.x.values), norm=norm, cmap=cmap) 

# plot the colorbar
cbar = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=cax, shrink=0.75, location='bottom')
cbar.ax.tick_params(labelsize=16)

fig.add_subplot(111, frameon=False)    #create new axes for axis labels
plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
plt.text(0.45, 0.065, "x (GCD)", fontsize=22)
plt.savefig(f"/glade/u/home/jwillson/dynamical-core/figures/{test_case}_{grid}_{resolution}/precip_composite.png", 
            dpi=300, bbox_inches='tight')