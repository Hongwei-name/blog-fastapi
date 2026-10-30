from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.schemas.post import PostCreate, PostRead, PostUpdate
from app.services.post import PostService

# 本模块负责 HTTP 层：接收并校验请求、调用 Service、将业务结果转换为 HTTP 响应。
# 数据库查询和写入放在 Repository 中，避免路由函数直接操作 ORM。
router = APIRouter()


# 空路径表示文章集合本身；本路由器会由上层统一挂载到 API 版本前缀下。
@router.post("", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_in: PostCreate,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> PostRead:
    """创建文章。

    请求路径为 `POST /api/v1/posts`，请求体是 JSON。FastAPI 会先校验 `PostCreate`：
    `title` 必须为 1 到 200 个字符，`content` 不能为空；校验通过后才调用 Service。

    参数：
        post_in: 已解析、校验通过的创建数据。
        session: 由依赖系统提供的异步数据库会话。

    返回：创建后的文章，响应字段由 `PostRead` 定义。
    状态码：`201` 表示创建成功；请求体不符合 Schema 时返回 `422`。
    """
    # FastAPI 将 JSON 解析为 PostCreate 并校验；失败时返回 422，不会执行函数。
    # Depends 从 get_db_session 注入异步会话，当前接口不需要手动创建或关闭数据库连接。
    # 创建成功返回 201；PostRead 同时约束响应字段，并将 ORM 对象转换为 JSON。
    return await PostService(session).create(post_in)


@router.get("", response_model=list[PostRead])
async def list_posts(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[PostRead]:
    """分页获取文章列表。

    请求路径为 `GET /api/v1/posts`。`limit` 指本次最多返回多少条，默认 20、范围为
    1 到 100；`offset` 指从第几条记录开始，默认从 0 开始。两者用于控制分页窗口。

    参数：
        session: 由依赖系统提供的异步数据库会话。
        limit: 单次返回数量；小于 1 或大于 100 时返回 `422`。
        offset: 跳过的记录数；小于 0 时返回 `422`。

    返回：文章数组；没有符合条件的文章时返回空数组。成功状态码为 `200`。
    """
    # Query 声明分页参数边界：limit 为 1 到 100，offset 不小于 0。
    # 参数越界时会自动返回 422。
    # 路由只负责接收参数，分页查询由 Service 和 Repository 完成。
    return await PostService(session).list(limit=limit, offset=offset)


@router.get("/{post_id}", response_model=PostRead)
async def get_post(
    post_id: int,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> PostRead:
    """根据 ID 获取单篇文章。

    请求路径为 `GET /api/v1/posts/{post_id}`，其中 `post_id` 是文章的整数主键。

    参数：
        post_id: URL 路径中的文章 ID；不能转换为整数时返回 `422`。
        session: 由依赖系统提供的异步数据库会话。

    返回：找到时返回 `PostRead` 格式的文章，状态码为 `200`；文章不存在时返回 `404`。
    """
    # 路径参数会由 FastAPI 转换成 int；无法转换时会返回 422。
    post = await PostService(session).get(post_id)
    if post is None:
        # Service 用 None 表示记录不存在；在 HTTP 边界将它映射为 404 响应。
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    return post


@router.patch("/{post_id}", response_model=PostRead)
async def update_post(
    post_id: int,
    post_in: PostUpdate,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> PostRead:
    """局部更新一篇文章。

    请求路径为 `PATCH /api/v1/posts/{post_id}`。请求体只需提供要修改的字段；未提供
    的字段保持原值。`PostUpdate` 会校验标题和正文，并拒绝显式传入的 `null`。

    参数：
        post_id: URL 路径中的文章 ID。
        post_in: 本次要更新的字段；字段校验失败时返回 `422`。
        session: 由依赖系统提供的异步数据库会话。

    返回：更新后的 `PostRead` 文章，状态码为 `200`；文章不存在时返回 `404`。
    """
    # PATCH 表示局部更新：请求体只需包含要修改的字段；Repository 只写入实际提交的字段。
    # PostUpdate 会拒绝空值或不符合长度约束的字段，校验失败时 FastAPI 自动返回 422。
    post = await PostService(session).update(post_id, post_in)
    if post is None:
        # 更新前未找到目标文章时，返回 404，而不是伪装成更新成功。
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> Response:
    """删除一篇文章。

    请求路径为 `DELETE /api/v1/posts/{post_id}`。

    参数：
        post_id: URL 路径中的文章 ID。
        session: 由依赖系统提供的异步数据库会话。

    返回：删除成功返回 `204 No Content`，因此响应没有正文；文章不存在时返回 `404`。
    """
    # Service 返回布尔值表示是否找到并删除了文章；不存在时由路由转换为 404。
    deleted = await PostService(session).delete(post_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    # 删除成功使用 204，表示操作完成且响应不带正文。
    return Response(status_code=status.HTTP_204_NO_CONTENT)
