from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

# 一个进程通常复用一个 Engine；Engine 管理连接池，不代表每个请求共用一个 Session。
# pool_pre_ping 会在取出连接时检查连接是否仍可用。
engine = create_async_engine(get_settings().database_url, pool_pre_ping=True)
# 工厂负责为每个请求创建独立 AsyncSession；提交后保留对象属性，便于构造响应。
SessionFactory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db_session() -> AsyncIterator[AsyncSession]:
    """FastAPI 数据库依赖：提供一个请求范围内的异步 Session。

    使用 `async with` 保证请求处理结束后关闭 Session；路由通过 Depends 注入它，
    不需要手动管理连接。异常时退出上下文也会释放会话资源。
    """
    async with SessionFactory() as session:
        # 依赖函数在 yield 处把会话交给 endpoint，endpoint 返回后继续执行清理流程。
        yield session
