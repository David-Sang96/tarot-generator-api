from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.services.tarot import load_deck


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # Load and validate the deck at startup, so bad data stops the server early.
    load_deck()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(api_router)
