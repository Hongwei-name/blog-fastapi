from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = Field(default=None, min_length=1)

    @field_validator("title", "content")
    @classmethod
    def reject_null_values(cls, value: str | None) -> str | None:
        if value is None:
            raise ValueError("Fields cannot be null")
        return value


class PostRead(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
