import pandas as pd
from Networksecurity.exception.exception import NetworkSecurityException
from Networksecurity.logger.logger import logging
from Networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
import os,sys
from Networksecurity.entity.artifact_entity import DataingestionArtifact   
import pymongo
from typing import List
from sklearn.model_selection import train_test_split
import numpy as np
import certifi
ca= certifi.where()

from dotenv import load_dotenv
load_dotenv()

mongo_db_url = os.getenv("mongo_db_url")

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    def read_data_from_mongo(self) -> pd.DataFrame:
        try:
            print('Reading data from MongoDB...')
            self.mongo_client = pymongo.MongoClient(mongo_db_url, tls=True, tlsCAFile=ca, tlsAllowInvalidCertificates=True)
            self.database = self.mongo_client[self.data_ingestion_config.database_name]
            self.collection = self.database[self.data_ingestion_config.collection_name]
            df = pd.DataFrame(list(self.collection.find()))
            logging.info(f"Data read from MongoDB collection: {self.data_ingestion_config.collection_name} in database: {self.data_ingestion_config.database_name}")
            if '_id' in df.columns.to_list():
                df.drop('_id', axis=1, inplace=True)
            df.replace({'na': np.nan}, inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    def export_data_to_feature_store(self):
        try:
            data=self.read_data_from_mongo()
            print(f"Data shape: {data.shape}")
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            os.makedirs(os.path.dirname(feature_store_file_path), exist_ok=True)
            data.to_csv(feature_store_file_path, index=False, header=True)
            logging.info("Feature store data saved successfully.")
            return data
        except Exception as e:
            raise NetworkSecurityException(e, sys)

  
    def save_train_test_data(self, data: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(data, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=42)
            train_file_path=self.data_ingestion_config.train_file_path
            test_file_path=self.data_ingestion_config.test_file_path
            os.makedirs(os.path.dirname(train_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(test_file_path), exist_ok=True)
            train_set.to_csv(train_file_path, index=False, header=True)
            test_set.to_csv(test_file_path, index=False, header=True)
            
            logging.info("Train and test data saved successfully.")
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    def initiate_data_ingestion(self):
        try:
            data=self.export_data_to_feature_store()
            self.save_train_test_data(data)
            data_ingestion_artifact = DataingestionArtifact(
                            train_file_path=self.data_ingestion_config.train_file_path,
                            test_file_path=self.data_ingestion_config.test_file_path
                        )
            return data_ingestion_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
              