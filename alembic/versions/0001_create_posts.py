"""Create posts table.

Revision ID: 0001_create_posts
Revises:
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0001_create_posts"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """将数据库升级到本版本：创建文章表及标题索引。"""
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_posts")),
    )
    # 索引可加快按标题过滤或排序的查询；unique=False 表示标题允许重复。
    op.create_index(op.f("ix_posts_title"), "posts", ["title"], unique=False)


def downgrade() -> None:
    """回滚本版本；先删除依赖表的索引，再删除表本身。"""
    op.drop_index(op.f("ix_posts_title"), table_name="posts")
    op.drop_table("posts")
