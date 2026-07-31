import yaml
from Networksecurity.exception.exception import NetworkSecurityException
from Networksecurity.logger.logger import logging
import os, sys
import numpy as np
import dill
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
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

def write_yaml_file(file_path:str, content:dict=None, replace:bool=False)->None:
    """
    Writes a dictionary to a YAML file.
    
    Args:
        file_path (str): The path to the YAML file.
        content (dict): The dictionary to write to the YAML file.
        replace (bool): Whether to replace the existing file. Defaults to False.
        
    Returns:
        None
    """
    try:
        dir_path = os.path.dirname(file_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        if replace and os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, "w") as yaml_file:
            yaml.dump(content, yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def save_numpy_array_data(file_path:str, array:np.ndarray)->None:
    
    try:
        dir_path = os.path.dirname(file_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
def save_object(file_path:str, obj:object)->None:
    
    try:
        dir_path = os.path.dirname(file_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def load_object(file_path:str)->object:
    
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def load_numpy_array_data(file_path:str)->np.ndarray:
    
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def evaluate_models(x_train, y_train, models:dict, param:dict)->dict:
    try:
        report = {}
        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = param[list(models.keys())[i]]
            gs=GridSearchCV(model, para, cv=3)
            gs.fit(x_train, y_train)
            model.set_params(**gs.best_params_)
            model.fit(x_train, y_train)
            y_train_pred = model.predict(x_train)
            train_model_score =r2_score(y_true=y_train, y_pred=y_train_pred)
            report[list(models.keys())[i]] = train_model_score
        return report
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e