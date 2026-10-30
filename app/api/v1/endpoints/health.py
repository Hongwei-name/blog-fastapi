from fastapi import APIRouter

# endpoint router 只负责声明 HTTP 路径；最终路径由上层是否添加前缀决定。
router = APIRouter()


@router.get("/health", summary="Check service health")
async def health_check() -> dict[str, str]:
    """存活探针：进程能够响应请求时返回 200 和简单状态信息。

    此接口不访问数据库，因此只检查 Web 应用是否存活；它不代表数据库一定可用。
    """
    return {"status": "ok"}
