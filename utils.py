import yaml

def open_config(config):
    with open(config) as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
    return conf