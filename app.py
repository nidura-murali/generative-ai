from fastapi import FastAPI
from agent import MerchantSearchAgent
from merchant_api import MerchantApiClient

app = FastAPI()

merchant_api = MerchantApiClient("https://your-api-base-url")
agent = MerchantSearchAgent(merchant_api)

@app.post("/chat")
def chat(query: str):
    return {"response": agent.handle_query(query)}