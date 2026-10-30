"""集中导入 ORM 模型，便于 Alembic 加载所有模型元数据。"""

from app.models.post import Post

# 明确公开的模型符号，供其他模块通过 app.models 导入。
__all__ = ["Post"]
