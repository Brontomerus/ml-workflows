from typing import Callable

from fastapi import FastAPI
from core.logger import logging

from core.config import DEFAULT_RF_MODEL_PATH, DEFAULT_ENCODER_MODEL_PATH
from services.models import NFLArrestsModel


def _startup_model(app: FastAPI) -> None:
    model_path = DEFAULT_RF_MODEL_PATH
    enc_path = DEFAULT_ENCODER_MODEL_PATH
    model_instance = NFLArrestsModel(model_path, enc_path)
    app.state.model = model_instance


def _shutdown_model(app: FastAPI) -> None:
    app.state.model = None


def start_app_handler(app: FastAPI) -> Callable:
    def startup() -> None:
        logger.info("Running app start handler.")
        _startup_model(app)
    return startup


def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        logger.info("Running app shutdown handler.")
        _shutdown_model(app)
    return shutdown