from fastapi import FastAPI, Depends
from agents.merchantSearchAgent import MerchantSearchAgent

from sbcaAPIs.merchantMatch import MerchantApiClient
from sbcaAPIs.merchantsMetrics import MetricsApiClient
from utils.schemas import AppError, ErrorResponse
from fastapi.responses import JSONResponse
from core.settings import get_settings

app = FastAPI()
settings = get_settings()
merchant_api = MerchantApiClient(settings.SBCA_HOST)
merchantSearchAgent = MerchantSearchAgent(merchant_api)

@app.post("/locate-merchant")
def chat(query: str):
    return {"response": merchantSearchAgent.handle_merchant_search(query)}
    
@app.exception_handler(AppError)
async def app_error_handler(statusCode : str, errorMessage : str):
    body = ErrorResponse(
        errorCode=statusCode,
        errorMessage=errorMessage,
    )
    # Decide your status codes: map business codes to HTTP codes if needed
    status = statusCode
    return JSONResponse(status_code=status, content=body.model_dump())
