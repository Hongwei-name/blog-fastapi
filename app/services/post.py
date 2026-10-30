from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post
from app.repositories.post import PostRepository
from app.schemas.post import PostCreate, PostUpdate


class PostService:
    """文章业务层：组织用例流程，并隔离 API 路由与数据访问层。

    复杂业务规则（权限、状态转换、跨仓储事务等）适合放在这一层；
    当前示例把简单 CRUD 转交给 Repository。
    """

    def __init__(self, session: AsyncSession) -> None:
        # Repository 使用同一个请求 Session，保证一次用例中的数据库操作共享上下文。
        self.repository = PostRepository(session)

    async def create(self, post_in: PostCreate) -> Post:
        """创建用例目前只需委托数据层完成持久化。"""
        return await self.repository.create(post_in)

    async def get(self, post_id: int) -> Post | None:
        """查询用例保留 Repository 的可空结果，由 API 层决定如何映射为 HTTP 响应。"""
        return await self.repository.get(post_id)

    async def list(self, limit: int, offset: int) -> list[Post]:
        """把已校验的分页参数传递给数据层。"""
        return await self.repository.list(limit, offset)

    async def update(self, post_id: int, post_in: PostUpdate) -> Post | None:
        """先查找目标，再更新；不存在时返回 None，不在 Service 中依赖 FastAPI。"""
        post = await self.repository.get(post_id)
        if post is None:
            return None
        return await self.repository.update(post, post_in)

    async def delete(self, post_id: int) -> bool:
        """返回是否删除成功，让调用方自行决定如何呈现结果。"""
        post = await self.repository.get(post_id)
        if post is None:
            return False
        await self.repository.delete(post)
        return True
