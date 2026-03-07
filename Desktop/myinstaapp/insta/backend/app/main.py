from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI(title="Instagram Advanced Clone")

app.include_router(api_router)