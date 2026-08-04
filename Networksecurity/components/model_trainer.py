import os 
import sys

from Networksecurity.exception.exception import NetworkSecurityException
from Networksecurity.logger.logger import logging

from Networksecurity.entity.config_entity import ModelTrainerConfig
from Networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact

from Networksecurity.utils.ml_utils.model.estimator import NetworkModel
from Networksecurity.utils.main_util.utils import load_object, save_object , load_numpy_array_data, evaluate_models
from Networksecurity.utils.ml_utils.metric.classification_metric import  get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier 
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier

import mlflow

class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
            # Use SQLite database backend instead of filesystem
            mlflow.set_tracking_uri("sqlite:///mlflow.db")
            mlflow.set_experiment("NetworkSecurityExperiment")
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def track_mlflow(self, best_model, classification_train_metric):
        with mlflow.start_run():
            f1_score=classification_train_metric.f1_score
            precision_score=classification_train_metric.precision_score
            recall_score=classification_train_metric.recall_score

            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("precision_score", precision_score)
            mlflow.log_metric("recall_score", recall_score)

            mlflow.sklearn.log_model(best_model, 'model')
    def model_trainer(self, x_train, y_train, x_test, y_test):
        try:
            models={
                "LogisticRegression": LogisticRegression(verbose=1),
                "KNeighborsClassifier": KNeighborsClassifier(),
                "DecisionTreeClassifier": DecisionTreeClassifier(),
                "RandomForestClassifier": RandomForestClassifier(verbose=1),
                "GradientBoostingClassifier": GradientBoostingClassifier(verbose=1),
                "AdaBoostClassifier": AdaBoostClassifier()
            }
            parameters={
                "LogisticRegression": {},
                "KNeighborsClassifier": {
                    "n_neighbors": [3, 5, 7]
                },
                "DecisionTreeClassifier": {
                    "criterion": ['gini', 'entropy', 'log_loss'],
                    # "splitter": ['best', 'random'],
                    # "max_depth": ['sqrt', 'log2', None],
                },
                "RandomForestClassifier": {
                    "n_estimators": [50, 100, 200],
                },
                "GradientBoostingClassifier": {
                    'learning_rate': [0.01, 0.1, 0.2],
                    'subsample': [0.8, 0.9, 1.0],
                },
                "AdaBoostClassifier": {
                    'n_estimators': [50, 100, 200],
                    'learning_rate': [0.01, 0.1, 1.0],
                }
            }
            model_report: dict = evaluate_models(x_train=x_train, y_train=y_train, models=models, param=parameters)

            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            y_train_pred = models[best_model_name].predict(x_train)
            classification_train_metric = get_classification_score(y_true=y_train, y_pred=y_train_pred)
            #
            best_model=models[best_model_name]

            self.track_mlflow(best_model=best_model, classification_train_metric=classification_train_metric)


            y_test_pred = models[best_model_name].predict(x_test)

            best_model=models[best_model_name]

            classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)


            self.track_mlflow(best_model=best_model, classification_train_metric=classification_test_metric)
            
            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)

            network_model = NetworkModel(preprocessor=preprocessor, model=models[best_model_name])
            save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=network_model)

            save_object(file_path="final_models/model.pkl", obj=best_model)

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric
            )

            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path=self.data_transformation_artifact.transformed_train_file_path
            test_file_path=self.data_transformation_artifact.transformed_test_file_path

            train_arr=load_numpy_array_data(train_file_path)
            test_arr=load_numpy_array_data(test_file_path)

            x_train, y_train, x_test, y_test = (train_arr[:,:-1],train_arr[:, -1],test_arr[:,:-1],test_arr[:,-1])

            model=self.model_trainer(x_train=x_train, y_train=y_train,x_test=x_test, y_test=y_test)
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e