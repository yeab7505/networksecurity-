from Networksecurity.components.data_ingestion import DataIngestion
from Networksecurity.exception.exception import NetworkSecurityException
from Networksecurity.logger.logger import logging   
from Networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from Networksecurity.components.data_validation import DataValidation, DataValidationConfig
import os,sys
if __name__=='__main__':
    try:
        logging.info("Starting Data Ingestion")
        training_pipeline_config=TrainingPipelineConfig()
        data_ingestion_config=DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion=DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
        logging.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")
        logging.info("Starting Data Validation")
        data_validation_config=DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation=DataValidation(data_validation_config=data_validation_config, data_ingestion_artifact=data_ingestion_artifact)
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info(f"Data Validation Artifact: {data_validation_artifact}")
        logging.info("Data Validation Completed")
    except Exception as e:
        raise NetworkSecurityException(e,sys)