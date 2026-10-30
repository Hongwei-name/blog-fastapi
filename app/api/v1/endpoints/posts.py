from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.schemas.post import PostCreate, PostRead, PostUpdate
from app.services.post import PostService

router = APIRouter()


@router.post("", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_in: PostCreate,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> PostRead:
    return await PostService(session).create(post_in)


@router.get("", response_model=list[PostRead])
async def list_posts(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[PostRead]:
    return await PostService(session).list(limit=limit, offset=offset)


@router.get("/{post_id}", response_model=PostRead)
async def get_post(
    post_id: int,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> PostRead:
    post = await PostService(session).get(post_id)
    if post is None:
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
    post = await PostService(session).update(post_id, post_in)
    if post is None:
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
    deleted = await PostService(session).delete(post_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
