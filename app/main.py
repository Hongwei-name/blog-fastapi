from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.api.v1.endpoints import health
from app.core.config import get_settings
from app.db.session import engine


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield
    await engine.dispose()


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan,
    )
    application.include_router(api_router)
    application.include_router(health.router, tags=["health"])
    return application


app = create_app()
