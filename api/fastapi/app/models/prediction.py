from pydantic import BaseModel


class NFLArrestsPredictResult(BaseModel):
    arrests: str

