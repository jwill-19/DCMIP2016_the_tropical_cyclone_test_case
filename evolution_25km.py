'''
Author: Justin Willson
Description: This script creates figure 5 in the DCMIP2016: the tropical cyclone test
case manuscript.
'''
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from utils import open_config, open_dataset, get_plot_name, get_radprof_arr

conf = open_config("conf")             #get parameters from config file
test_case = conf['test_case']                   
grid = conf['grid']
resolution = conf['resolution']
res50 = '50km'                         #original resolution
day = conf['day']                      #begin time average after this day
height = conf['height']                #height of rprof to be plotted

model_conf = open_config('models')     #get list of models
models = []

for model in list(model_conf.keys()):  #get model names from config file
    if model_conf[model]['25km'] == True:
        models.append(model)
        
fig, ax = plt.subplots(2, 1, sharex=True, figsize=(12,12), tight_layout=True)

for ax, i in zip(ax.ravel(), range(2)):
    for model in models:
        if model == 'dynamico':                           #dynamico is 3 hourly
            time = data.time_counter.values/(60.0*60.0*24.0) 
        else:
            time = np.array([0.25*j for j in range(41)])  #standard DCMIP2016 time values
        
        if i == 0:
            file = f'/glade/u/home/jwillson/DCMIP2016_the_tropical_cyclone_test_case/trajectories/{test_case}_{grid}_{resolution}/{model}_trajectories.csv'
            ps_data = pd.read_csv(file)
            ps = ps_data[ps_data.columns[-2]]    #pressure is the second to last column
            ps = ps[:41]                         #only keep the first track in some 25km models                    
            ax.plot(time, ps/100, color=model_conf[model]['color'])
            
            #now use same procedure to plot original 50km curves on the same plot
            file = f'/glade/u/home/jwillson/DCMIP2016_the_tropical_cyclone_test_case/trajectories/{test_case}_{grid}_{res50}/{model}_trajectories.csv'
            ps_data = pd.read_csv(file)
            ps = ps_data[ps_data.columns[-2]]    
            ps = ps[:41]                                            
            ax.plot(time, ps/100, linestyle='dashed', alpha=0.5, color=model_conf[model]['color'])
        else:
            file = f'/glade/u/home/jwillson/DCMIP2016_the_tropical_cyclone_test_case/wind_rad_prof/{test_case}_{grid}_{resolution}/{model}_{height}.txt'  
            rprof = get_radprof_arr(file) #extract radial profile from text file
            max_wind = []

            for i in range(time.shape[0]):  #calculate max wind at each timestep
                max_wind.append(np.max(rprof[i,:]))

            max_wind = max_wind[:41]        #only keep the first track in some 25km models
            ax.plot(time, max_wind, color=model_conf[model]['color'])
            
            #now use same procedure to plot original 50km curves on the same plot
            file = f'/glade/u/home/jwillson/DCMIP2016_the_tropical_cyclone_test_case/wind_rad_prof/{test_case}_{grid}_{res50}/{model}_{height}.txt'  
            rprof = get_radprof_arr(file) #extract radial profile from text file
            max_wind = []

            for i in range(time.shape[0]):  #calculate max wind at each timestep
                max_wind.append(np.max(rprof[i,:]))

            max_wind = max_wind[:41]        #only keep the first track in some 25km models
            ax.plot(time, max_wind, linestyle='dashed', alpha=0.5, color=model_conf[model]['color'])
        
    if i == 0:                                   #set labels and fontsizes
        ax.set_ylabel("Pressure (hPa)", fontsize=22)
    else:
        ax.set_xlabel("Days", fontsize=22)
        ax.set_ylabel("Wind Speed (m/s)", fontsize=22)
        
    ax.tick_params(axis='x', labelsize=16)
    ax.tick_params(axis='y', labelsize=16)

handles = []  #add custom legend
for model in models:
    handles.append(mpatches.Patch(color=model_conf[model]['color'], label=get_plot_name(model)))
ax.legend(handles=handles, bbox_to_anchor=(0.91, -0.15), ncol=5, fontsize=16)
plt.savefig(f"figures/{test_case}_{grid}_{resolution}/evolution_combined.png", dpi=300, bbox_inches='tight')