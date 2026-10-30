from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.api.v1.endpoints import health
from app.core.config import get_settings
from app.db.session import engine


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """管理应用的启动与关闭生命周期。

    `yield` 前可放置启动时初始化逻辑；`yield` 后执行关闭清理。
    当前应用在关闭时释放异步数据库引擎及其连接池。
    """
    yield
    await engine.dispose()


def create_app() -> FastAPI:
    """创建并配置 FastAPI 实例。

    使用工厂函数能让生产入口和测试代码创建相同配置的应用；测试还可以为
    返回的实例单独覆盖依赖，而不必复制一份应用配置。
    """
    settings = get_settings()
    application = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan,
    )
    # 版本化业务接口统一由 api_router 挂载；健康检查保留在根路径 /health。
    application.include_router(api_router)
    application.include_router(health.router, tags=["health"])
    return application


# Uvicorn 使用 `app.main:app` 时会加载此模块级应用实例。
app = create_app()
