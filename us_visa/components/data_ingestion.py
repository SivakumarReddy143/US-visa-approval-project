import os
import sys

from us_visa.exception import USvisaException
from sklearn.model_selection import train_test_split

from us_visa.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact
from us_visa.constant import *

import pandas as pd
from pandas import DataFrame

from us_visa.data_access.usvisa_data import USvisaData

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
            pass
        except Exception as e:
            raise USvisaException(e,sys)
    def export_data_to_feature_store(self):
        try:
            usvisa_data=USvisaData()
            dataframe=usvisa_data.export_collection_as_dataframe(COLLECTION_NAME)
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
            
        except Exception as e:
            raise USvisaException(e,sys)
    def split_data_as_train_test(self,dataframe:DataFrame):
        try:
            train_data,test_data=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            os.makedirs(self.data_ingestion_config.data_ingested_dir,exist_ok=True)
            train_data.to_csv(self.data_ingestion_config.train_file_path,index=False,header=True)
            test_data.to_csv(self.data_ingestion_config.test_file_path,index=False,header=True)
            
        except Exception as e:
            raise USvisaException(e,sys)
        
    def initiate_data_ingestion(self):
        try:
            pass
            dataframe=self.export_data_to_feature_store()
            self.split_data_as_train_test(dataframe)
            data_ingestion_artifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.train_file_path,
                                                          test_file_path=self.data_ingestion_config.test_file_path
                                                          )
            return data_ingestion_artifact
        except Exception as e:
            raise USvisaException(e,sys)