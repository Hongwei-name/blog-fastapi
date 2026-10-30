from fastapi import APIRouter

from app.api.v1.api import api_v1_router
from app.core.config import get_settings

# 顶层路由聚合器负责统一施加版本前缀，不承载具体业务处理。
api_router = APIRouter()
# include_router 会把前缀与子路由路径拼接，例如得到 /api/v1/posts。
api_router.include_router(api_v1_router, prefix=get_settings().api_v1_prefix)
