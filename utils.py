import yaml
import xarray as xr

def open_config(filename):
    """
    Opens .yml files for a specific variable.
    
    Inputs:
    filename (string): Name of file.
    
    Outputs:
    conf (loaded .yml file): Contents of .yml file
    in a nested dictionary.
    
    """
    config = f"/glade/u/home/jwillson/dynamical-core/{filename}.yml"
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
    
    