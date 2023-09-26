from fastapi import FastAPI

from app.base import api_router

app = FastAPI()

app.include_router(api_router)
