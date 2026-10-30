from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PostCreate(BaseModel):
    """创建文章时允许客户端提交的字段及其校验规则。"""

    # 标题不能为空且最多 200 个字符；正文至少需要一个字符。
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)


class PostUpdate(BaseModel):
    """局部更新 Schema：默认值 None 表示字段可以不出现在请求体中。"""

    # 字段类型暂时允许 None，以表达“未提供”的默认状态；显式 null 由校验器拒绝。
    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = Field(default=None, min_length=1)

    @field_validator("title", "content")
    @classmethod
    def reject_null_values(cls, value: str | None) -> str | None:
        """拒绝 JSON null，避免把数据库的非空列更新为空值。"""
        if value is None:
            raise ValueError("Fields cannot be null")
        return value


class PostRead(BaseModel):
    """API 对外返回的文章结构；不直接暴露任意 ORM 内部字段。"""

    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    # 允许 Pydantic 从 ORM 对象属性读取字段，而不要求先手动构造字典。
    model_config = ConfigDict(from_attributes=True)
