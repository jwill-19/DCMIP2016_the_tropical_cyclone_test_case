import yaml
import xarray as xr
import numpy as np

def open_config(filename):
    """
    Opens .yml files for a specific variable.
    
    Inputs:
    filename (string): Name of file.
    
    Outputs:
    conf (loaded .yml file): Contents of .yml file
    in a nested dictionary.
    
    """
    config = f"/glade/u/home/jwillson/dynamical-core/config/{filename}.yml"
    with open(config) as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
    return conf

def open_dataset(files, model):
    """
    Open Xarray Dataset.
    
    Inputs:
    files (nested dictionary): opened config file.
    model (string): model name.
    
    Outputs:
    Data (Xarray Dataset): Data
    
    """
    conf = open_config("conf")
    test_case = conf['test_case']
    grid = conf['grid']
    resolution = conf['resolution']
    
    file = files[f"{test_case}"][f"{grid}"][f"{resolution}"][model]
    data = xr.open_dataset(file, decode_times=False)
    
    return data
    
def get_radprof_arr(filename):
    """
    Extracts the radial profile array from the TempestExtremes
    output file. 
    
    Inputs:
        filename (string): Name of file
        
    Outputs:
        radprof_arr (np.ndarray): Output array of radial profiles.
        rsize_arr (np.array): Output array for radius size.
    """
    radprof_arr = []
    with open(filename, 'r') as file:
        for line in file:
            rprof = line.split()[-1][2:-2].split(',') #get array of numbers as strings
            if len(rprof) == 1:
                continue
            else:
                for i in range(len(rprof)):
                    rprof[i] = float(rprof[i])  #convert each element to a float
            
            radprof_arr.append(rprof)
            
    return np.array(radprof_arr)