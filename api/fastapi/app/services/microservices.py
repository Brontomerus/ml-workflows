import boto3
import json

from core.config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, ARRESTS_FUNCTION
from core.logger import logging
from models.prediction import NFLArrestsPredictResult
from models.payload import (NFLArrestPredictionPayload, payload_categorical_to_list,
                            payload_numerical_to_list, payload_continuous_to_list)


# categorical: list = ["2", "San Fransisco", "Pittsburg", "SF", "NFL WEST", "open", "8"]      
# numerical: list = [63400, 2, 0]
# continuous: list = [] 


class NFLArrestsMicroservice(object):

    def __init__(self):
        self.accesskey = AWS_ACCESS_KEY
        self.secretkey = AWS_SECRET_KEY
        self.region = AWS_REGION
        self.function = ARRESTS_FUNCTION
    #     self._init_microservice()

    # def _init_microservice(self):
    #     self.client = boto3.client('lambda', region_name=self.region, aws_access_key_id=self.accesskey, aws_secret_access_key=self.secretkey)

    def _prepare_features(self, payload: NFLArrestPredictionPayload) -> dict:
        return {
                "categorical": payload_categorical_to_list(payload), 
                "numerical": payload_numerical_to_list(payload), 
                "continuous": payload_continuous_to_list(payload)
                }

    def _invoke(self, features: dict) -> NFLArrestsPredictResult:
        result = self.client.invoke(FunctionName=ARRESTS_FUNCTION, InvocationType='RequestResponse', Payload=json.dumps(features))
        return json.loads(result['Payload'].read().decode('utf-8'))


#_invoke(_prepare_features(payload))