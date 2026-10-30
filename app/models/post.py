from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Post(Base):
    """文章数据库实体；类属性通过 SQLAlchemy 映射为 posts 表的列。"""

    __tablename__ = "posts"

    # 未显式指定类型时，SQLAlchemy 根据 Python 类型推断整数主键列。
    id: Mapped[int] = mapped_column(primary_key=True)
    # 标题限制 200 字符并建立索引，便于按标题检索；正文使用不定长 Text。
    title: Mapped[str] = mapped_column(String(200), index=True)
    content: Mapped[str] = mapped_column(Text)
    # 由数据库在插入时填入创建时间；timezone=True 表示使用带时区的时间类型。
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    # 插入时设置默认值，ORM 更新该对象时由 onupdate 生成新的更新时间。
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
