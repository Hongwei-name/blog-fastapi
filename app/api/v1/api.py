from fastapi import APIRouter

from app.api.v1.endpoints import posts

api_v1_router = APIRouter()
api_v1_router.include_router(posts.router, prefix="/posts", tags=["posts"])
