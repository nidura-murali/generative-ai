from fastapi import FastAPI
from agent import MerchantSearchAgent
from merchant_api import MerchantApiClient
from metrics_api import MetricsApiClient
from schemas import AppError, ErrorResponse
from fastapi.responses import JSONResponse

app = FastAPI()

merchant_api = MerchantApiClient("https://your-api-base-url")
metrics_api = MetricsApiClient("http://localhost:8081")
agent = MerchantSearchAgent(merchant_api, metrics_api)

@app.post("/locate-merchant")
def chat(query: str):
    return {"response": agent.handle_query(query)}
    
@app.exception_handler(AppError)
async def app_error_handler(statusCode : str, errorMessage : str):
    body = ErrorResponse(
        errorCode=statusCode,
        errorMessage=errorMessage,
    )
    # Decide your status codes: map business codes to HTTP codes if needed
    status = statusCode
    return JSONResponse(status_code=status, content=body.model_dump())
