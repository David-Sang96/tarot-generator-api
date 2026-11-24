from fastapi import APIRouter

from app.api.v1.routes import tarot

api_router = APIRouter(prefix="/v1/api")
api_router.include_router(tarot.router)
