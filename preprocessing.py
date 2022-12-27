import yaml
import numpy as np
import xarray as xr
from utils import open_config, open_dataset
from conversions import hybrid_to_pressure, pressure_to_height
from interpolation import height_interp

#configuration for preprocessing: see dynamical-core/config/conf.yml

conf = open_config("conf")
test_case = conf['test_case']
grid = conf['grid']
resolution = conf['resolution']
all_models = conf['all_models']

if all_models == True:
    model_conf = open_config("models")
    models = list(model_conf.keys())
else:
    models = conf['models']

vars_ = conf['vars']
val = conf['val']
existing_files = conf['existing_files']

#loop through all desired variables and models

for var in vars_:
    for model in models:
        if (model == 'dynamico') and (var == 'PRECL'): #dynamico doesn't have a PRECL variable
            continue
        
        files = open_config(var)        #access all filenames of a particular variable
        
        if existing_files == True:      #open existing file if it exists
            f = f"/glade/work/jwillson/dynamical-core/{test_case}_{grid}_{resolution}/{model}.{var}.nc"
            data = xr.open_dataset(f, decode_times=False)   
        else:            
            data = open_dataset(files, model)  #open NetCDF dataset of specified variable and model
            
            if model == 'fv3_dzlow': #save attributes, switch units, and add calendar by switching to CAM-SE attributes 
                data1 = open_dataset(files, 'cam-se')
                attrs = data1.time.attrs
                data = data.assign_coords(time=(data1.time.values))
                data = data.assign_coords(time=data.time.assign_attrs(attrs))
                variables = dict(data.data_vars)      #get list of variables and remove desired variable from list
                var_names = list(variables.keys())
                var_names.pop(var_names.index(f"{var}")) 
                data = data.drop_vars(var_names) #drop all other variables from dataset while keeping metadata and coordinates
                
            elif model == 'dynamico':
                attrs = data.time_counter.attrs   #save attributes and switch units
                attrs['units'] = 'days since 2000-01-01 00:00:00'
                                                  #remove bounds and rename coordinate to time 
                data = data.drop_vars(["time_instant_bounds", "time_counter_bounds"])
                data = data.rename({'time_counter':'time'})
                                                  #assign new values and attributes to time
                data = data.assign_coords(time=[i*(10.0/80.0) for i in range(80)])
                data = data.assign_coords(time=data.time.assign_attrs(attrs))
                
            elif model == 'acme-a':
                #change time 'units' attribute to 'days since 2000-01-01 00:00:00' and add cam-se calendar attribute
                #since calendar is unknown
                data1 = open_dataset(files, model)
                attrs = data1.time.attrs
                attrs['units'] = 'days since 2000-01-01 00:00:00'
                attrs['calendar'] = 'noleap'
                data = data.assign_coords(time=(data1.time.values))
                data = data.assign_coords(time=data.time.assign_attrs(attrs))
                
            elif model == 'fvm': #fvm does not have a time coordinate so we add the cam-se time coordinate
                data1 = open_dataset(files, 'cam-se')
                attrs = data1.time.attrs
                data = data.assign_coords(time=(data1.time.values))
                data = data.assign_coords(time=data.time.assign_attrs(attrs))
            
            elif model.count('csu') == 1:  #add calendar attribute
                data1 = open_dataset(files, model)
                attrs = data1.time.attrs
                attrs['calendar'] = 'noleap'
                data = data.assign_coords(time=(data1.time.values))
                data = data.assign_coords(time=data.time.assign_attrs(attrs))
        
            elif model == 'nicam':
                if var == 'PRECL':  #avoids error where times are all copied to 0 by assigning cam-se time coord with nicam attrs
                    data1 = open_dataset(files, 'cam-se')
                    data2 = open_dataset(files, model)
                    attrs = data2.time.attrs
                    data = data.assign_coords(time=data1.time.values)
                    data = data.assign_coords(time=data.time.assign_attrs(attrs))
            
            else:
                pass        #no changes necessary
            
        #if wind variable interpolate, assign each height to an individual variable
        if var == "U" or var == "V":
            interp = height_interp(val, var, model) 
            if type(val) == list:
                for i in range(len(val)):
                    data = data.assign({f"{var}{str(val[i])[:-2]}":(("time", "lat", "lon"), interp[:,i,:,:])})
            else:
                data = data.assign({f"{var}{str(val[i])[:-2]}":(("time", "lat", "lon"), interp)})
            
        #save as file, if permission denied save as new file
        try:
            data.to_netcdf(f"/glade/work/jwillson/dynamical-core/{test_case}_{grid}_{resolution}/{model}.{var}.nc")
        except:
            data.to_netcdf(f"/glade/work/jwillson/dynamical-core/{test_case}_{grid}_{resolution}/{model}.{var}.1.nc")
            print(f"Run {model} postprocessing")