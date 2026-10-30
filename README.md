# Blog FastAPI

基于 FastAPI、SQLAlchemy 2.0 和 Alembic 的博客后端模板，采用 API、Service、Repository 分层。

## 环境要求

- Python 3.11+
- 推荐使用 [uv](https://docs.astral.sh/uv/)

## 快速开始

```bash
uv sync --extra dev
cp .env.example .env
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

默认使用本地 SQLite，无需另行安装数据库。启动后访问 `http://127.0.0.1:8000/docs` 查看交互式 API 文档。

也可以使用 pip：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
alembic upgrade head
uvicorn app.main:app --reload
```

## 项目结构

```text
app/
	api/v1/endpoints/  HTTP 路由与依赖
	core/              配置
	db/                SQLAlchemy 基础类与会话
	models/            ORM 模型
	repositories/      数据访问
	schemas/           请求与响应模型
	services/          业务逻辑
alembic/             数据库迁移
tests/               API 测试
```

## API

- `GET /health`：服务存活检查
- `POST /api/v1/posts`：创建文章
- `GET /api/v1/posts`：分页列出文章
- `GET /api/v1/posts/{post_id}`：获取文章
- `PATCH /api/v1/posts/{post_id}`：更新文章
- `DELETE /api/v1/posts/{post_id}`：删除文章

文章列表支持 `limit` 和 `offset` 查询参数。

## 配置

环境变量可通过 `.env` 设置，字段名使用 `APP_` 前缀，例如 `APP_DATABASE_URL`。默认数据库为 `sqlite+aiosqlite:///./blog.db`。切换 PostgreSQL 时设置：

```dotenv
APP_DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/blog
```

新增或修改模型后，生成并应用迁移：

```bash
uv run alembic revision --autogenerate -m "describe change"
uv run alembic upgrade head
```

## 开发检查

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
```
