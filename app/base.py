from fastapi import APIRouter

from app.auth import route_login, route_register
from app.images import route_image

api_router = APIRouter(
    prefix="/api",
)
api_router.include_router(route_login.router, prefix="", tags=["Login"])
api_router.include_router(route_register.router, prefix="", tags=["Register"])
api_router.include_router(route_image.router, prefix="", tags=["Image"])
