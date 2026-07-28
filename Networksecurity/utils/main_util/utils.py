import yaml
from Networksecurity.exception.exception import NetworkSecurityException
from Networksecurity.logger.logger import logging
import os, sys
import numpy as np
import dill
import pickle

def read_yaml_file(file_path:str)->dict:
    """
    Reads a YAML file and returns its contents as a dictionary.
    
    Args:
        file_path (str): The path to the YAML file.
        
    Returns:
        dict: The contents of the YAML file as a dictionary.
    """
    try:
        with open(file_path, "r") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)