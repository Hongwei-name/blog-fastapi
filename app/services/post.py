from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post
from app.repositories.post import PostRepository
from app.schemas.post import PostCreate, PostUpdate


class PostService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = PostRepository(session)

    async def create(self, post_in: PostCreate) -> Post:
        return await self.repository.create(post_in)

    async def get(self, post_id: int) -> Post | None:
        return await self.repository.get(post_id)

    async def list(self, limit: int, offset: int) -> list[Post]:
        return await self.repository.list(limit, offset)

    async def update(self, post_id: int, post_in: PostUpdate) -> Post | None:
        post = await self.repository.get(post_id)
        if post is None:
            return None
        return await self.repository.update(post, post_in)

    async def delete(self, post_id: int) -> bool:
        post = await self.repository.get(post_id)
        if post is None:
            return False
        await self.repository.delete(post)
        return True
