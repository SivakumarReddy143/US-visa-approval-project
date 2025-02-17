import sys
from typing import Tuple

import numpy as np
import pandas as pd
from pandas import DataFrame
from us_visa.utils.main_utils import *
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score,r2_score,f1_score,precision_score, recall_score
from neuro_mf import ModelFactory

from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.entity.config_entity import *
from us_visa.entity.artifact_entity import *
from us_visa.entity.estimator import USvisaModel

class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact,
                 model_trainer_config:ModelTrainerConfig
                 ):
        try:
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_config=model_trainer_config
        except Exception as e:
            raise USvisaException(e,sys)
        
    def get_model_object_and_report(self,train:np.array,test:np.array)->Tuple[object,object]:
        try:
            model_factory=ModelFactory(model_config_path=self.model_trainer_config.model_config_file_path)
            x_train,y_train,x_test,y_test=train[:,:-1],train[:,-1],test[:,:-1],test[:,-1]
            
            best_model_detail=model_factory.get_best_model(
                X=x_train,y=y_train,base_accuracy=self.model_trainer_config.expected_score
            )
            model_obj=best_model_detail.best_model
            y_pred=model_obj.predict(x_test)
            
            accuracy=accuracy_score(y_test,y_pred)
            precision_score_value=precision_score(y_test,y_pred)
            recall_score_value=recall_score(y_test,y_pred)
            f1_score_value=f1_score(y_test,y_pred)
            metric_artifact=ClassificationMetricArtifact(f1_score=f1_score_value,
                                                         precision_score=precision_score_value,
                                                         recall_score=recall_score_value
                                                         )
            return best_model_detail,metric_artifact
        except Exception as e:
            raise USvisaException(e,sys)
        
    def initiate_model_trainer(self, ) -> ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")
        """
        Method Name :   initiate_model_trainer
        Description :   This function initiates a model trainer steps
        
        Output      :   Returns model trainer artifact
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            train_arr = load_numpy_array_data(filepath=self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array_data(filepath=self.data_transformation_artifact.transformed_test_file_path)
            
            best_model_detail ,metric_artifact_values = self.get_model_object_and_report(train=train_arr, test=test_arr)
            
            preprocessing_obj = load_object(filepath=self.data_transformation_artifact.transformed_object_file_path)


            if best_model_detail.best_score < self.model_trainer_config.expected_score:
                logging.info("No best model found with score more than base score")
                raise Exception("No best model found with score more than base score")

            usvisa_model = USvisaModel(preprocessing_object=preprocessing_obj,
                                       trained_model_object=best_model_detail.best_model)
            logging.info("Created usvisa model object with preprocessor and model")
            logging.info("Created best model file path.")
            save_object(self.model_trainer_config.trained_model_file_path, usvisa_model)

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_filepath=self.model_trainer_config.trained_model_file_path,
                metric_artifact=metric_artifact_values
            )
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise USvisaException(e, sys) from e
        

