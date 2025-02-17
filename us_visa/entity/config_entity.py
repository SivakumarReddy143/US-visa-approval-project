import os
from datetime import datetime
from us_visa.constant import *
from dataclasses import dataclass

TIMESTAMP = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')

@dataclass
class TrainingPipelineConfig:
    pipeline_name: str = PIPELINE_NAME
    artifact_dir = os.path.join(ARTIFACT_DIR, TIMESTAMP)
    timestamp = TIMESTAMP
    
@dataclass
class DataIngestionConfig:
    data_ingestion_dir = os.path.join(TrainingPipelineConfig.artifact_dir,DATA_INGESTION_DIR_NAME)
    feature_store_file_path = os.path.join(data_ingestion_dir,DATA_INGESTION_FEATURE_STORE,FILE_NAME)
    data_ingested_dir = os.path.join(data_ingestion_dir,DATA_INGESTION_INGESTED_DIR)
    train_file_path = os.path.join(data_ingested_dir,TRAIN_FILE_NAME)
    test_file_path = os.path.join(data_ingested_dir,TEST_FILE_NAME)
    train_test_split_ratio = DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
    
@dataclass
class DataValidationConfig:
    data_validation_dir = os.path.join(TrainingPipelineConfig.artifact_dir,DATA_VALIDATION_DIR)
    drift_report_dir = os.path.join(data_validation_dir,DATA_VALIDATION_DRIFT_REPORT_DIR)
    drift_report_file_path = os.path.join(drift_report_dir,DATA_VALIATION_DRIFT_REPORT_FILE_NAME)
    
@dataclass
class DataTransformationConfig:
    data_transformation_dir = os.path.join(TrainingPipelineConfig.artifact_dir,DATA_TRANSFORMATION_DIR_NAME)
    transformed_train_file_path = os.path.join(data_transformation_dir,DATA_TRANSFORMATION_TRANSFORMED_DIR_NAME,TRAIN_FILE_NAME.replace('csv','npy'))
    transformed_test_file_path = os.path.join(data_transformation_dir,DATA_TRANSFORMATION_TRANSFORMED_DIR_NAME,TEST_FILE_NAME.replace('csv','npy'))
    transformed_object_file_path = os.path.join(data_transformation_dir,DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,PREPROCESSING_OBJECT_FILE_NAME)
    
@dataclass
class ModelTrainerConfig:
    model_trainer_dir = os.path.join(TrainingPipelineConfig.artifact_dir,MODEL_TRAINER_DIR)
    trained_model_file_path = os.path.join(model_trainer_dir,MODEL_TRAINER_TRAINED_MODEL_DIR,MODEL_FILE_NAME)
    expected_score = MODEL_TRAINER_EXPECTED_SCORE
    model_config_file_path = MODEL_TRAINER_MODEL_CONFIG_FILE_PATH
    

@dataclass
class ModelEvaluationConfig:
    changed_thresold_score:float = MODEL_EVALUATION_CHANGED_THRESOLD_SCORE
    bucket_name = MODEL_BUCKET_NAME
    s3_model_key_path = MODEL_FILE_NAME
    
@dataclass
class ModelPusherConfig:
    bucket_name = MODEL_BUCKET_NAME
    s3_model_key_path = MODEL_FILE_NAME
    
@dataclass
class USvisaPredictorConfig:
    model_file_path = MODEL_FILE_NAME
    model_bucket_name = MODEL_BUCKET_NAME
    