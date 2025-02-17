import os
from datetime import date

COLLECTION_NAME = "visa_data"
DATABASE_NAME = "US_VISA"
MONGO_DB_URL="MONGO_DB_URL"

PIPELINE_NAME = "us_visa"
ARTIFACT_DIR="artifacts"

TARGET_COLUMN = "case_status"
FILE_NAME= "us_visa.csv"

TRAIN_FILE_NAME= "train.csv"
TEST_FILE_NAME= "test.csv"
CURRENT_YEAR= date.today().year

SCHEMA_FILE_PATH=os.path.join('config','schema.yaml')
PREPROCESSING_OBJECT_FILE_NAME="preprocessing.pkl"
MODEL_FILE_NAME="model.pkl"

AWS_ACCESS_KEY_ID_ENV_KEY = "AWS_ACCESS_KEY_ID"
AWS_SECRET_KEY_ID_ENV_KEY = "AWS_SECRET_ACCESS_KEY"
REGION_NAME = "us-east-1"

"""
Data ingestion constants
"""

DATA_INGESTION_COLLECTION_NAME: str = "us_visa"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2

"""
Data Validation constants
"""

DATA_VALIDATION_DIR: str = "data_validation"
DATA_VALIDATION_DRIFT_REPORT_DIR : str = "drift_report"
DATA_VALIATION_DRIFT_REPORT_FILE_NAME : str = "report.yaml"

"""
DATA TRANSFORMATION CONSTANTS
"""

DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DIR_NAME: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"

"""
Model training constant definitions
"""

MODEL_TRAINER_DIR: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH: str = os.path.join("config","model.yaml") 


"""
Model evaluation related constant
"""

MODEL_EVALUATION_CHANGED_THRESOLD_SCORE: float = 0.02
MODEL_BUCKET_NAME: str = "usvisa-siva143"
MODEL_PUSHER_S3_KEY = "model_registry"

APP_HOST = "0.0.0.0"
APP_PORT = 8080