import yaml
import numpy as np
import xarray as xr
from utils import open_config, open_dataset
from conversions import hybrid_to_pressure, pressure_to_height

def height_interp(val, var, model):
    """
    Interpolates the data to new height values using linear interpolation.
    
    Inputs:
        val (float or list): numerical value or list of values 
                              to interpolate to
        var (string): variable name
        model (string): model name
    
    Outputs:
        interp (nd array): array of interpolated values
    """
    model_conf = open_config("models")
    files = open_config(var)
    data = open_dataset(files, model)
    
    # interpolate using xarray method if model uses height levels
    # accepts float or array as input
    if model_conf[model]['levels'] == 'height': 
        if var == "U":
            interp = data.U.interp(lev=val).values
        if var == "V":
            interp = data.V.interp(lev=val).values
            
    else:
        if var == "U":
            if model == "acme-a": # acme-a uses lowercase variable names
                arr = data.u.values
            else:
                arr = data.U.values
        
        if var == "V":
            if model == "acme-a":
                arr = data.v.values
            else:
                arr = data.V.values
                
        if model == 'dynamico': # dynamico uses time_counter instead of time
            time = data.time_counter.values/(60.0*60.0*24.0)
        else:
            time = data.time.values
            
        if model == 'gem': # gem has a geopotential height variable
            Z_files = open_config("Z")
            Z_data = open_dataset(Z_files, model)
            Z = Z_data.PHII.values        
        else:              # use conversion function
            Z = pressure_to_height(model)
        
        if type(val) == list: # new array has dimensions (time,lev,lat,lon)
            new_shape = (time.shape[0], len(val), data.lat.shape[0], data.lon.shape[0])
            interp = np.zeros(new_shape)

            for i in range(time.shape[0]): # loop through all points and times
                for j in range(data.lat.shape[0]):
                    for k in range(data.lon.shape[0]):
                        sub_arr = arr[i,:,j,k]  # get appropriate slices of array
                        Z_ijk = Z[i,:,j,k]
                        
                        # reverse height array so it is strictly increasing
                        # also reverse variable array to preserve correct relationship
                        # use np.interp function for fastest interpolation
                        if model_conf[model]['positive'] == 'down': 
                            interp[i,:,j,k] = np.interp(val, Z_ijk[::-1], sub_arr[::-1])
                        else:
                            interp[i,:,j,k] = np.interp(val, Z_ijk, sub_arr)
        
        # same process except new array has dimensions (time,lat,lon)
        else: 
            new_shape = (time.shape[0], data.lat.shape[0], data.lon.shape[0])
            interp = np.zeros(new_shape)

            for i in range(time.shape[0]):
                for j in range(data.lat.shape[0]):
                    for k in range(data.lon.shape[0]):
                        sub_arr = arr[i,:,j,k]
                        Z_ijk = Z[i,:,j,k]

                        if model_conf[model]['positive'] == 'down':
                            interp[i,j,k] = np.interp(val, Z_ijk[::-1], sub_arr[::-1])
                        else:
                            interp[i,j,k] = np.interp(val, Z_ijk, sub_arr)
                            
    return interp