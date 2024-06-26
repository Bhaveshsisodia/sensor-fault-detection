from sensor.entity.artifact_entity import ClassificationMetricArtifact
from sensor.exception import SensorException
import os , sys
from sensor.logger import logging
from sklearn.metrics import f1_score , precision_score , recall_score



def get_classification_score(y_true,y_pred) -> ClassificationMetricArtifact:
    try:
        model_f1_score = f1_score(y_true, y_pred)
        model_recall_score = recall_score(y_true, y_pred)
        model_precision_score = precision_score(y_true, y_pred)

        classification_metirc= ClassificationMetricArtifact(f1_score=model_f1_score,
                                            precision_score=model_precision_score,
                                            recall_score=model_recall_score)

        logging.info(f"classification metrics are :{classification_metirc}")

        return classification_metirc
    except Exception as e:
        raise SensorException(e, sys) from e