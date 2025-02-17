import os
import sys
import yaml
import numpy as np
import dill
from pandas import DataFrame
from us_visa.exception import USvisaException

def read_yaml_file(filepath)->dict:
    try:
        with open(filepath, 'rb') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise USvisaException(e, sys)

def write_yaml_file(filepath:str,content:object,replace:bool=False):
    try:
        if replace:
            if os.path.exists(filepath):
                os.remove(filepath)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath,'w') as file:
            yaml.dump(content,file)
    except Exception as e:
        raise USvisaException(e, sys)
    
def load_object(filepath:str):
    try:
        with open(filepath,'rb') as file:
            return dill.load(file)
    except Exception as e:
        raise USvisaException(e, sys)
    

def save_numpy_array_data(filepath:str,array:np.array):
    try:
        os.makedirs(os.path.dirname(filepath),exist_ok=True)
        with open(filepath,'wb')as file:
            np.save(file,array)
    except Exception as e:
        raise USvisaException(e, sys)
    
def load_numpy_array_data(filepath:str)->np.array:
    try:
        with open(filepath,'rb') as file:
            return np.load(filepath)
    except Exception as e:
        raise USvisaException(e, sys)
    
def save_object(filepath:str,obj:object)->None:
    try:
        os.makedirs(os.path.dirname(filepath),exist_ok=True)
        with open(filepath,'wb') as file:
            dill.dump(obj,file)
    except Exception as e:
        raise USvisaException(e, sys)
    
def drop_columns(df:DataFrame,cols:list)->DataFrame:
    try:
        df=df.drop(columns=cols,axis=1)
        return df
    except Exception as e:
        raise USvisaException(e, sys)