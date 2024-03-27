from typing import List

import pickle
import numpy as np
from core.logger import logging

from core.messages import NO_VALID_PAYLOAD
from models.payload import (NFLArrestPredictionPayload, payload_to_list)
from models.prediction import NFLArrestsPredictResult


class NFLArrestsModel(object):

    def __init__(self, model_path, prepro_path):
        self.model_path = model_path
        self.prepro_path = prepro_path
        self._load_local_model()

    def _load_local_model(self):
        self.model = pickle.load(open(self.model_path,'rb'))
        self.enc = pickle.load(open(self.prepro_path,'rb'))

    def _pre_process(self, payload: NFLArrestPredictionPayload) -> List:
        logging.debug("Pre-processing payload.")
        result = np.asarray(payload_to_list(payload)).reshape(1, -1)
        return result

    def _post_process(self, prediction: np.ndarray) -> NFLArrestsPredictResult:
        logging.debug("Post-processing prediction.")
        result = prediction.tolist()
        arrests = NFLArrestsPredictResult(Arrests=result)
        return arrests

    def _predict(self, features: List) -> np.ndarray:
        logging.debug("Predicting.")
        prediction_result = self.model.predict(features)
        return prediction_result

    def predict(self, payload: NFLArrestPredictionPayload):
        if payload is None:
            raise ValueError(NO_VALID_PAYLOAD.format(payload))

        pre_processed_payload = self._pre_process(payload)
        prediction = self._predict(pre_processed_payload)
        logging.info(prediction)
        post_processed_result = self._post_process(prediction)

        return post_processed_result