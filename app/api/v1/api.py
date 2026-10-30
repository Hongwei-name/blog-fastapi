from fastapi import APIRouter

from app.api.v1.endpoints import posts

# v1 路由注册表：新增 v1 业务模块后，在这里 include 对应的 router。
api_v1_router = APIRouter()
# 文章子路由负责集合和单条资源操作，统一放在 /posts 路径下。
api_v1_router.include_router(posts.router, prefix="/posts", tags=["posts"])
