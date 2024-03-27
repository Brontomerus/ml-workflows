from fastapi import APIRouter, Depends
from starlette.requests import Request

from core import security
from core.logger import logging

from models.payload import NFLArrestPredictionPayload
from models.prediction import NFLArrestsPredictResult
from services.microservices import NFLArrestsMicroservice
#from services.models import NFLArrestsModel # uncomment if using in-app model


router = APIRouter()


@router.post("/predict", response_model=NFLArrestsPredictResult, name="predict")
def post_predict(request: Request, authenticated: bool = Depends(security.validate_request), block_data: NFLArrestPredictionPayload = None) -> NFLArrestsPredictResult:
    
    # If I were to use the initialized model in the application itself with core.event_handlers, id use below:
    # model: NFLArrestsModel = request.app.state.model

    model: NFLArrestsMicroservice = NFLArrestsMicroservice()
    prediction: NFLArrestsPredictResult = model._invoke(model._prepare_features(block_data))

    return prediction