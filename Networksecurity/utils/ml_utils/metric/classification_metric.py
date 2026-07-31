from Networksecurity.entity.artifact_entity import classificationMetricArtifact
from Networksecurity.exception.exception import NetworkSecurityException
from sklearn.metrics import  precision_score, recall_score, f1_score
import sys

def get_classification_score(y_true, y_pred) -> classificationMetricArtifact:
    try:
        model_f1_score=f1_score(y_true, y_pred)
        model_precision_score=precision_score(y_true, y_pred)
        model_recall_score=recall_score(y_true, y_pred)
        classification_metric_artifact=classificationMetricArtifact(f1_score=model_f1_score, precision_score=model_precision_score, recall_score=model_recall_score)
        return classification_metric_artifact
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e