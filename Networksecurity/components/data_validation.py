from Networksecurity.entity.config_entity import DataValidationConfig
from Networksecurity.exception.exception import NetworkSecurityException
import sys
from Networksecurity.logger.logger import logging
from Networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from Networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from Networksecurity.utils.main_util.utils import read_yaml_file


class DataValidation: 
    def __init__(self, data_validation_config: DataValidationConfig, data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self. schma_config =read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)