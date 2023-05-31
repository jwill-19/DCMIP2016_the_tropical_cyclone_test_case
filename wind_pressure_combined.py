'''
Author: Justin Willson
Description: This script creates figures 2 and 6 in the DCMIP2016: the tropical cyclone test
case manuscript.
'''
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from utils import open_config, open_dataset, get_radprof_arr, get_plot_name
from curve_fitting import quadratic

conf = open_config("conf")      #open config file and get parameters
test_case = conf['test_case']
grid = conf['grid']
resolution = conf['resolution']
height = conf['height']

model_conf = open_config("models")           #open model config file

if resolution == "25km":                     #get model names from config file
    models = []
    for model in list(model_conf.keys()):        
        if model_conf[model]['25km'] == True:
            models.append(model)
else:
    models = list(model_conf.keys())

fig, ax = plt.subplots(figsize=(12,7), tight_layout=True)
ax.set_xlabel("Pressure (hPa)", fontsize=22)
ax.set_ylabel("Wind (m/s)", fontsize=22)
ax.tick_params(axis='x', labelsize=16)
ax.tick_params(axis='y', labelsize=16)

for model in models:
    u_files = open_config("U")
    data = open_dataset(u_files, model)  #open example dataset (for time arrays)

    if model == 'dynamico':              #get time array in days
        time = data.time_counter.values/(60.0*60.0*24.0) 
    elif model == 'fvm':
        time = np.array([0.25*i for i in range(41)])
    elif model == 'nicam':
        time = data.time.values/(60.0*24.0)
    else:
        time = data.time.values

    file1 = f'/glade/u/home/jwillson/dynamical-core/wind_rad_prof/{test_case}_{grid}_{resolution}/{model}_{height}.txt'
    rprof = get_radprof_arr(file1)       #extract radial profile from text file
    maxw = []
    for i in range(time.shape[0]):       #append the maximum wind for each time
        maxw.append(np.max(rprof[i,:]))
    
    file2 = f'/glade/u/home/jwillson/dynamical-core/trajectories/{test_case}_{grid}_{resolution}/{model}_trajectories.csv'
    ps_data = pd.read_csv(file2)
    ps = ps_data[ps_data.columns[-2]]    #minimum surface pressure is the second to last column
    ps = ps/100
    
    maxw = maxw[:41]                     #only keep the first track in some 25km models
    ps = ps[:41]
                                         #fit a quadratic function to the data
    popt, pcov = curve_fit(quadratic, ps, maxw)     
    ps_fit = np.linspace(np.min(ps), np.max(ps), 1000)
    maxw_fit = quadratic(ps_fit, popt[0], popt[1], popt[2])
    
    ax.plot(ps, maxw, '.', markersize=10, color=model_conf[model]['color'], label=get_plot_name(model))
    ax.plot(ps_fit, maxw_fit, '-', color=model_conf[model]['color'])
    
ax.legend(fontsize=16)
plt.savefig(f"figures/{test_case}_{grid}_{resolution}/wind_pressure_all_{height}.png", dpi=300, bbox_inches='tight')