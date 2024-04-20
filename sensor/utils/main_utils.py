import yaml
from sensor.exception import SensorException
import sys, os

def read_yaml_file(file_path:str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise SensorException(e,sys) from  e


def write_yaml_file(file_path: str, content:object , replace:bool=False) -> None:
    try:
# sourcery skip: merge-nested-ifs
        if replace and os.path.exists(file_path):
            os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise SensorException(e, sys) from e
