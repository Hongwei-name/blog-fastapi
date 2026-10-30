from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

# 为数据库对象生成稳定且唯一的名称，便于 Alembic 在不同数据库之间管理迁移。
# 例如索引使用 ix_ 前缀、主键约束使用 pk_ 前缀。
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """所有 ORM 模型继承的声明式基类。

    模型类会注册到共享的 metadata；Alembic 使用它比较模型与数据库结构。
    """

    metadata = MetaData(naming_convention=NAMING_CONVENTION)
