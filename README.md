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
uv run uvicorn app.main:app --host 0.0.0.0 --reload
```

默认使用本地 SQLite，无需另行安装数据库。启动后访问 `http://127.0.0.1:8000/docs` 查看交互式 API 文档。

也可以使用 pip：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
alembic upgrade head
uvicorn app.main:app  --host 0.0.0.0 --reload
```

## 项目结构

```text
.
├── app/
│   ├── api/
│   │   ├── router.py                 汇总并挂载 API 路由
│   │   └── v1/
│   │       ├── api.py                注册 v1 版本的路由
│   │       └── endpoints/
│   │           ├── health.py         健康检查接口
│   │           └── posts.py          文章 HTTP 接口
│   ├── core/
│   │   └── config.py                 应用配置与环境变量
│   ├── db/
│   │   ├── base.py                   ORM 声明基类与命名约定
│   │   └── session.py                异步数据库引擎与会话依赖
│   ├── models/                       SQLAlchemy ORM 模型
│   ├── repositories/                 数据访问逻辑
│   ├── schemas/                      请求参数与响应数据模型
│   ├── services/                     业务逻辑
│   └── main.py                       FastAPI 应用入口
├── alembic/
│   ├── versions/                     数据库迁移版本
│   └── env.py                        Alembic 迁移环境配置
├── tests/
│   ├── conftest.py                   测试客户端与数据库 fixture
│   └── test_posts.py                 API 接口测试
├── .env.example                      环境变量配置示例
├── alembic.ini                       Alembic 命令配置
├── pyproject.toml                    项目元数据、依赖与工具配置
└── uv.lock                           锁定依赖版本
```

新增业务模块时，可沿用文章模块的分层方式：由 `endpoints` 处理 HTTP 请求与响应，`services` 编排业务规则，`repositories` 负责数据库读写，`schemas` 定义 API 数据结构，`models` 定义 ORM 表结构。

## API

- `GET /health`：服务存活检查
- `POST /api/v1/posts`：创建文章
- `GET /api/v1/posts`：分页列出文章
- `GET /api/v1/posts/{post_id}`：获取文章
- `PATCH /api/v1/posts/{post_id}`：更新文章
- `DELETE /api/v1/posts/{post_id}`：删除文章

文章列表支持 `limit` 和 `offset` 查询参数。

### HTTP 状态码

状态码表示服务器处理请求的结果：`2xx` 表示成功，`4xx` 通常表示请求或参数有问题，`5xx` 表示服务器处理时发生错误。

| 状态码 | 含义 | 本项目中的常见场景 |
| --- | --- | --- |
| `200 OK` | 请求成功 | 查询文章列表或详情、更新文章成功 |
| `201 Created` | 资源创建成功 | 创建文章成功 |
| `204 No Content` | 操作成功，没有响应正文 | 删除文章成功 |
| `404 Not Found` | 找不到请求的资源 | 文章 ID 不存在，或请求了不存在的路径 |
| `405 Method Not Allowed` | 路径存在，但不支持当前 HTTP 方法 | 对只支持 `GET` 的接口发送 `POST` 请求 |
| `422 Unprocessable Entity` | 请求参数未通过校验 | 标题为空、文章字段缺失、`limit` 超出 `1-100` 或 `offset` 小于 `0` |
| `500 Internal Server Error` | 服务器内部发生未预期错误 | 服务异常；检查服务端日志，通常不是修改请求参数可以解决的 |

错误响应通常会包含 `detail` 字段，用来说明具体原因。收到 `404` 时检查 URL 和文章 ID；收到 `422` 时根据 `detail` 修正请求参数。

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
