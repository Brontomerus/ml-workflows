from starlette.config import Config
from starlette.datastructures import Secret

import os
import databases
 
APP_VERSION = "0.0.1"
APP_NAME = "Project to operate a serverless machine learning architecture"
API_PREFIX = "/api"
 
 
# config = Config(".env")
 
# DATABASE_URL = config('DATABASE_URL', cast=databases.DatabaseURL)
 
# API_KEY: Secret = config("API_KEY", cast=Secret, default=False)
# IS_DEBUG: bool = config("IS_DEBUG", cast=bool, default=False)
 
# DEFAULT_RF_MODEL_PATH: str = config("DEFAULT_RF_MODEL_PATH", default=False)
# DEFAULT_ENCODER_MODEL_PATH: str = config("DEFAULT_ENCODER_MODEL_PATH", default=False)
 
# AWS_ACCESS_KEY: Secret = config("AWS_ACCESS_KEY", cast=Secret, default=False)
# AWS_SECRET_KEY: Secret = config("AWS_SECRET_KEY", cast=Secret, default=False)
 
 
API_KEY: Secret = os.getenv("API_KEY")
IS_DEBUG: bool = False
DEFAULT_RF_MODEL_PATH: str = "./serialized_models/encoder.pkl"
DEFAULT_ENCODER_MODEL_PATH: str = "./serialized_models/rf_regressor.pkl"


AWS_REGION: str = "us-east-2"
ARRESTS_FUNCTION: str = "Project-Predict-Arrests"
AWS_ACCESS_KEY: Secret = os.getenv("AWS_ACCSES_KEY")
AWS_SECRET_KEY: Secret = os.getenv("AWS_SECRET_KEY")

