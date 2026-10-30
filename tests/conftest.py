import asyncio

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app import models  # noqa: F401
from app.db.base import Base
from app.db.session import get_db_session
from app.main import create_app


@pytest.fixture
def client(tmp_path):
    """为每个测试创建独立 SQLite 数据库和 TestClient，避免测试间共享数据。"""
    database_path = tmp_path / "test.db"
    engine = create_async_engine(f"sqlite+aiosqlite:///{database_path}")
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async def create_schema():
        # create_all 需要同步回调，因此通过 AsyncConnection.run_sync 调用元数据建表。
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    asyncio.run(create_schema())

    async def override_get_db_session():
        # 测试请求使用临时数据库会话，不会读写开发者本机的 blog.db。
        async with session_factory() as session:
            yield session

    application = create_app()
    # FastAPI 允许替换 Depends 依赖；键必须是 endpoint 使用的原依赖函数对象。
    application.dependency_overrides[get_db_session] = override_get_db_session
    with TestClient(application) as test_client:
        yield test_client
    # 测试结束后恢复依赖并释放连接池，防止状态泄漏到其他测试。
    application.dependency_overrides.clear()
    asyncio.run(engine.dispose())
