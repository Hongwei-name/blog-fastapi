from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from app import models  # noqa: F401
from app.core.config import get_settings
from app.db.base import Base

# Alembic 命令运行时的上下文；数据库 URL 与应用共享同一份 Settings 配置。
config = context.config
config.set_main_option("sqlalchemy.url", get_settings().database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 导入模型后，所有 ORM 表都会登记到 Base.metadata，供 --autogenerate 比对。
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """离线模式只生成 SQL，不建立数据库连接。"""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    """在给定连接上配置迁移上下文并执行当前版本迁移。"""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """在线模式创建异步引擎，再通过 run_sync 运行 Alembic 的同步迁移函数。"""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


if context.is_offline_mode():
    # `alembic upgrade --sql` 等命令走离线分支，不连接真实数据库。
    run_migrations_offline()
else:
    import asyncio

    # Alembic 迁移操作本身是同步 API，因此由 asyncio.run 驱动上面的异步连接管理。
    asyncio.run(run_migrations_online())
