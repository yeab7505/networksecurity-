
import os

from dotenv import load_dotenv
import sys
import json
import pandas as pd
import numpy as np
# pyrefly: ignore [missing-import]
import pymongo
from Networksecurity.exception.exception import NetworkSecurityException
from Networksecurity.logger.logger import logging   
load_dotenv()

mongo_db_url = os.getenv("mongo_db_url")


import certifi
ca = certifi.where()

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def cv_to_dson_convertor(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records = json.loads(data.T.to_json()).values()
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def insert_data_to_mongo(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records

            self.mongo_client=pymongo.MongoClient(mongo_db_url, tls=True, tlsCAFile=ca, tlsAllowInvalidCertificates=True)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

if __name__=='__main__':
    FILE_PATH = r"C:\Users\yeabsira\Documents\ml project\cyber security project\Networksecurity\phisingData.csv"
    DATABASE_NAME = "NetworkSecurity"
    COLLECTION_NAME = "NetworkData"
    networkobj=NetworkDataExtract()
    records=networkobj.cv_to_dson_convertor(FILE_PATH)
    inseted=networkobj.insert_data_to_mongo(records,DATABASE_NAME,COLLECTION_NAME)