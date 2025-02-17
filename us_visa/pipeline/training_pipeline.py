import sys
from us_visa.components.model_evaluation import ModelEvaluation
from us_visa.components.model_pusher import ModelPusher
from us_visa.exception import USvisaException
from us_visa.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig, ModelPusherConfig, ModelTrainerConfig, ModelEvaluationConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact, ModelEvaluationArtifact, ModelPusherArtifact, ModelTrainerArtifact
from us_visa.components.data_ingestion import DataIngestion
from us_visa.components.data_validation import DataValidation
from us_visa.logger import logging
from us_visa.components.data_transformation import DataTransformation
from us_visa.components.model_trainer import ModelTrainer


class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config=DataIngestionConfig()
        self.data_validation_config=DataValidationConfig()
        self.data_transformation_config=DataTransformationConfig()
        self.model_trainer_config=ModelTrainerConfig()
        self.model_evaluation_config = ModelEvaluationConfig()
        self.model_pusher_config = ModelPusherConfig()
        
    def start_dataingestion(self)->DataIngestionArtifact:
        try:
            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifacts=data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifacts
        except Exception as e:
            raise USvisaException(e,sys)
    
    def start_datavalidation(self,data_ingestion_artifact:DataIngestionArtifact):
        try:
            data_validation=DataValidation(datavalidation_config=self.data_validation_config,data_ingestion_artifact=data_ingestion_artifact)
            data_validation_artifact=data_validation.initiate_data_validation()
            return data_validation_artifact
        except Exception as e:
            raise USvisaException(e,sys)
    
    def start_datatransformation(self,data_ingestion_artifact,data_validation_artifact:DataValidationArtifact):
        try:
            data_transformation=DataTransformation(data_ingestion_artifact=data_ingestion_artifact,
                                                   data_validation_artifact=data_validation_artifact,
                                                   data_transformation_config=self.data_transformation_config
                                                   )
            data_transformation_artifact=data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise USvisaException(e,sys)
    
    def start_model_training( self,data_transformation_artifact:DataTransformationArtifact):
        try:
            model_trainer=ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                       model_trainer_config=self.model_trainer_config
                                       )
            model_trainer_artifact=model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise USvisaException(e,sys)
    
    def start_model_evaluation(self, data_ingestion_artifact: DataIngestionArtifact,
                               model_trainer_artifact: ModelTrainerArtifact) -> ModelEvaluationArtifact:
        """
        This method of TrainPipeline class is responsible for starting modle evaluation
        """
        try:
            model_evaluation = ModelEvaluation(model_eval_config=self.model_evaluation_config,
                                               data_ingestion_artifact=data_ingestion_artifact,
                                               model_trainer_artifact=model_trainer_artifact)
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            return model_evaluation_artifact
        except Exception as e:
            raise USvisaException(e, sys)
        
    
    def start_model_pusher(self, model_evaluation_artifact: ModelEvaluationArtifact) -> ModelPusherArtifact:
        """
        This method of TrainPipeline class is responsible for starting model pushing
        """
        try:
            model_pusher = ModelPusher(model_evaluation_artifact=model_evaluation_artifact,
                                       model_pusher_config=self.model_pusher_config
                                       )
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            return model_pusher_artifact
        except Exception as e:
            raise USvisaException(e, sys)
        

    
    def run_pipeline(self, ) -> None:
        """
        This method of TrainPipeline class is responsible for running complete pipeline
        """
        try:
            data_ingestion_artifact = self.start_dataingestion()
            data_validation_artifact = self.start_datavalidation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_datatransformation(data_ingestion_artifact=data_ingestion_artifact,
                                                                         data_validation_artifact=data_validation_artifact
                                                                         )
            model_trainer_artifact = self.start_model_training(data_transformation_artifact)
            model_evaluation_artifact = self.start_model_evaluation(data_ingestion_artifact=data_ingestion_artifact,
                                                                    model_trainer_artifact=model_trainer_artifact)
            
            if not model_evaluation_artifact.is_model_accepted:
                logging.info(f"Model not accepted.")
                return None
            model_pusher_artifact = self.start_model_pusher(model_evaluation_artifact=model_evaluation_artifact)
            
        except Exception as e:
            raise USvisaException(e,sys)