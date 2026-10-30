from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """集中声明应用配置，并从进程环境变量或 `.env` 文件读取值。

    环境变量使用 `APP_` 前缀，例如 `APP_DATABASE_URL`；环境变量优先于 `.env`
    中的同名配置。把配置集中在此处，避免各模块自行读取环境变量。
    """

    # API 文档中显示的服务名称。
    app_name: str = "Blog API"
    # 是否开启 FastAPI 调试模式；部署环境通常保持关闭。
    debug: bool = False
    # 业务 API 的统一版本前缀，由 app/api/router.py 挂载。
    api_v1_prefix: str = "/api/v1"
    # 默认使用本地异步 SQLite；部署时可替换为 asyncpg PostgreSQL URL。
    database_url: str = "sqlite+aiosqlite:///./blog.db"

    # BaseSettings 据此加载 `.env`，只接受 APP_ 前缀配置，并忽略无关变量。
    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """返回进程内缓存的配置实例，避免每次请求都重新读取配置文件。"""
    return Settings()
