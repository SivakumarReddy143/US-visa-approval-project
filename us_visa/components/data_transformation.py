import sys
import numpy as np
import pandas as pd

from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler,OrdinalEncoder,PowerTransformer
from sklearn.compose import ColumnTransformer

from us_visa.constant import TARGET_COLUMN,CURRENT_YEAR,SCHEMA_FILE_PATH
from us_visa.entity.config_entity import DataTransformationConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.utils.main_utils import *
from us_visa.entity.estimator import TargetValueMapping

class DataTransformation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig
                 ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise USvisaException(e,sys)
    
    @staticmethod
    def readData(filepath):
        try:
            return pd.read_csv(filepath)
        except Exception as e:
            raise USvisaException(e,sys)
    
    def get_transformer_object(self)->Pipeline:
        try:
            numeric_transformer=StandardScaler()
            oh_transformer=OneHotEncoder()
            or_transformer=OrdinalEncoder()
            
            oh_columns=self.schema_config['oh_columns']
            or_columns=self.schema_config['or_columns']
            transform_columns=self.schema_config['transform_columns']
            num_features=self.schema_config['num_features']
            
            transform_pipe = Pipeline(steps=[
                ('transformer', PowerTransformer(method='yeo-johnson'))
            ])
            
            preprocessor = ColumnTransformer([
                ('OneHotEncoder',oh_transformer,oh_columns),
                ('OrdinalEncoder',or_transformer,or_columns),
                ('Transformer',transform_pipe,transform_columns),
                ('StandardScaler',numeric_transformer,num_features,)
            ])
            
            return preprocessor
            
        except Exception as e:
            raise USvisaException(e,sys)
    def initiate_data_transformation(self)->DataIngestionArtifact:
        try:
            if self.data_validation_artifact.validation_status:
                preprocessor=self.get_transformer_object()
                
                train_df=DataTransformation.readData(filepath=self.data_ingestion_artifact.trained_file_path)
                test_df = DataTransformation.readData(filepath=self.data_ingestion_artifact.test_file_path)
                
                input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
                target_feature_train_df=train_df[TARGET_COLUMN]
                input_feature_train_df['company_age']= CURRENT_YEAR - input_feature_train_df['yr_of_estab']
                drop_cols=self.schema_config['drop_columns']
                input_feature_train_df.drop(columns=drop_cols)
                target_feature_train_df=target_feature_train_df.replace(TargetValueMapping()._asdict())
                
                input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
                target_feature_test_df=test_df[TARGET_COLUMN]
                input_feature_test_df['company_age']=CURRENT_YEAR-input_feature_test_df['yr_of_estab']
                drop_cols=self.schema_config['drop_columns']
                input_feature_test_df=input_feature_test_df.drop(columns=drop_cols,axis=1)
                target_feature_test_df=target_feature_test_df.replace(TargetValueMapping()._asdict())
                
                input_feature_train_df=preprocessor.fit_transform(input_feature_train_df)
                input_feature_test_df=preprocessor.transform(input_feature_test_df)
                
                smt=SMOTEENN(sampling_strategy='minority')
                
                input_feature_train_final,target_feature_train_final=smt.fit_resample(input_feature_train_df,
                                                                                    target_feature_train_df
                                                                                    )
                input_feature_test_final,target_feature_test_final=smt.fit_resample(input_feature_test_df,
                                                                                    target_feature_test_df
                                                                                    )
                train_arr=np.c_[
                    input_feature_train_final,np.array(target_feature_train_final)
                ]
                
                test_arr = np.c_[
                    input_feature_test_final,np.array(target_feature_test_final)
                ]
                
                save_object(self.data_transformation_config.transformed_object_file_path,preprocessor)
                save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,train_arr)
                save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,test_arr)
                
                data_transformation_artifact=DataTransformationArtifact(
                    transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                    transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                    transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
                )
                
                return data_transformation_artifact
            
            else:
                raise Exception(self.data_validation_artifact.message)
            
        except Exception as e:
            raise USvisaException(e,sys)
