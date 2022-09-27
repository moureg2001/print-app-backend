import os
import yaml
from datetime import datetime, timedelta


def load_config():
    dir_root = os.path.dirname(os.path.abspath(__file__))
    with open(dir_root + "/config.yaml", "r") as yaml_file:
        return yaml.load(yaml_file, Loader=yaml.FullLoader)


config = load_config()
