from Networksecurity.constants.training_pipeline import SAVED_MODEL_DIR, SAVED_MODEL_FILE_NAME

import os 
import sys

from Networksecurity.exception.exception import NetworkSecurityException
from Networksecurity.logger.logger import logging

class NetworkModel:
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e, sys) 

    def predict(self, X):
        try:
            X_transform = self.preprocessor.transform(X)
            return self.model.predict(X_transform)
        except Exception as e:
            raise NetworkSecurityException(e, sys)