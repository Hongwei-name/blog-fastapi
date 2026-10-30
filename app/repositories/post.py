from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate


class PostRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, post_in: PostCreate) -> Post:
        post = Post(**post_in.model_dump())
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)
        return post

    async def get(self, post_id: int) -> Post | None:
        return await self.session.get(Post, post_id)

    async def list(self, limit: int, offset: int) -> list[Post]:
        statement = select(Post).order_by(Post.id).limit(limit).offset(offset)
        result = await self.session.scalars(statement)
        return list(result.all())

    async def update(self, post: Post, post_in: PostUpdate) -> Post:
        for field, value in post_in.model_dump(exclude_unset=True).items():
            setattr(post, field, value)
        await self.session.commit()
        await self.session.refresh(post)
        return post

    async def delete(self, post: Post) -> None:
        await self.session.delete(post)
        await self.session.commit()
