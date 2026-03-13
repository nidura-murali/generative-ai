from pydantic import BaseModel
from typing import Optional
from enum import Enum

class IdType(str, Enum):
    MERCHANT_ID = "MERCHANT_ID"
    MMH_ID = "MMH_ID"
    TAX_ID = "TAX_ID"

class ExtractionResult(BaseModel):
    countryCode: Optional[str]
    idType: Optional[IdType]
    idValue: Optional[str]
    confidence: Optional[str]
    needsClarification: Optional[bool]
    clarificationQuestion: Optional[str]

class ErrorResponse(BaseModel):
    errorCode: str
    errorMessage: str   


class AppError(Exception):
    def __init__(self, errorCode: str, errorMessage: str):
        super().__init__(errorMessage)
        self.errorCode = errorCode
        self.errorMessage = errorMessage
