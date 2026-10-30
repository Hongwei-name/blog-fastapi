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
    database_path = tmp_path / "test.db"
    engine = create_async_engine(f"sqlite+aiosqlite:///{database_path}")
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async def create_schema():
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    asyncio.run(create_schema())

    async def override_get_db_session():
        async with session_factory() as session:
            yield session

    application = create_app()
    application.dependency_overrides[get_db_session] = override_get_db_session
    with TestClient(application) as test_client:
        yield test_client
    application.dependency_overrides.clear()
    asyncio.run(engine.dispose())
