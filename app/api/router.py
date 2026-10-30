from fastapi import APIRouter

from app.api.v1.api import api_v1_router
from app.core.config import get_settings

api_router = APIRouter()
api_router.include_router(api_v1_router, prefix=get_settings().api_v1_prefix)
