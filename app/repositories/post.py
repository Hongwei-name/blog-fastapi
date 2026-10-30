from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate


class PostRepository:
    """文章数据访问层：把 SQLAlchemy 查询和持久化细节集中在此处。

    Repository 不负责 HTTP 状态码，也不决定 API 响应格式；这些职责属于上层。
    """

    def __init__(self, session: AsyncSession) -> None:
        # 注入当前请求的 Session，所有方法通过同一个会话执行数据库操作。
        self.session = session

    async def create(self, post_in: PostCreate) -> Post:
        """将已验证的创建 Schema 转为 ORM 实体并写入数据库。"""
        # Schema 只包含客户端允许提交的字段，model_dump 转成普通关键字参数。
        post = Post(**post_in.model_dump())
        self.session.add(post)
        # commit 将事务持久化；refresh 从数据库读取自增 ID 和时间默认值。
        await self.session.commit()
        await self.session.refresh(post)
        return post

    async def get(self, post_id: int) -> Post | None:
        """按主键读取单条记录；不存在时 SQLAlchemy 返回 None。"""
        return await self.session.get(Post, post_id)

    async def list(self, limit: int, offset: int) -> list[Post]:
        """按主键升序读取一页文章，确保分页结果顺序稳定。"""
        # limit 限制结果数量，offset 跳过前面的记录；参数边界已由 API 层校验。
        statement = select(Post).order_by(Post.id).limit(limit).offset(offset)
        result = await self.session.scalars(statement)
        return list(result.all())

    async def update(self, post: Post, post_in: PostUpdate) -> Post:
        """只把请求中实际出现的字段写入 ORM 对象，然后提交更新。"""
        # exclude_unset=True 区分“客户端没传字段”和“字段使用默认值”；未传字段不变。
        for field, value in post_in.model_dump(exclude_unset=True).items():
            setattr(post, field, value)
        await self.session.commit()
        # 重新读取数据库值，确保返回对象包含更新后的时间戳等字段。
        await self.session.refresh(post)
        return post

    async def delete(self, post: Post) -> None:
        """标记 ORM 实体为删除并提交事务。"""
        await self.session.delete(post)
        await self.session.commit()
