from  datetime import datetime 
import os 
import sys

from bson import timestamp
from Networksecurity.exception.exception import NetworkSecurityException
from Networksecurity.constants import training_pipeline

class TrainingPipelineConfig:
    def __init__(self):
        try:
            self.pipeline_name=training_pipeline.PIPELINE_NAME
            self.artifact_name=training_pipeline.ARTIFACT_DIR
            self.train_test_split_ratio=training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
            self.timestamp:str=datetime.now().strftime("%m%d%Y__%H%M%S")
            self.artifact_dir=os.path.join(self.artifact_name, self.timestamp)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        try:
            self.data_ingestion_dir=os.path.join(training_pipeline_config.artifact_dir,training_pipeline.DATA_INGESTION_DIR_NAME)
            self.feature_store_file_path=os.path.join(self.data_ingestion_dir,training_pipeline_config.DATA_INGESTION_FEATURE_STORE_DIR,training_pipeline.FILE_NAME)
            self.train_file_path=os.path.join(self.data_ingestion_dir,training_pipeline_config.DATA_INGESTION_INGESTED_DIR,training_pipeline.TRAIN_FILE_NAME)
            self.test_file_path=os.path.join(self.data_ingestion_dir,training_pipeline_config.DATA_INGESTION_INGESTED_DIR,training_pipeline.TEST_FILE_NAME)
            self.train_test_split_ratio=training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
            self.collection_name=training_pipeline.DATA_INGESTION_COLLECTION_NAME
            self.database_name=training_pipeline.DATA_INGESTION_DATABASE_NAME
        except Exception as e:
            raise NetworkSecurityException(e,sys)