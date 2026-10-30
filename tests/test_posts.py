def test_health_check(client):
    """健康检查应返回 200 和固定的存活状态。"""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_post_lifecycle(client):
    """验证文章从创建、查询、局部更新到删除的完整 API 生命周期。"""
    create_response = client.post(
        "/api/v1/posts",
        json={"title": "First post", "content": "Hello, blog!"},
    )

    assert create_response.status_code == 201
    post = create_response.json()
    assert post["title"] == "First post"

    list_response = client.get("/api/v1/posts?limit=10&offset=0")
    assert [item["id"] for item in list_response.json()] == [post["id"]]

    update_response = client.patch(
        f"/api/v1/posts/{post['id']}",
        json={"title": "Updated post"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated post"

    delete_response = client.delete(f"/api/v1/posts/{post['id']}")
    assert delete_response.status_code == 204

    missing_response = client.get(f"/api/v1/posts/{post['id']}")
    assert missing_response.status_code == 404


def test_post_validation(client):
    """请求数据不满足 Schema 约束时，FastAPI 应返回 422。"""
    response = client.post("/api/v1/posts", json={"title": "", "content": "body"})

    assert response.status_code == 422


def test_post_update_rejects_null(client):
    """显式 null 不等于省略字段，局部更新应拒绝该值。"""
    response = client.patch("/api/v1/posts/1", json={"title": None})

    assert response.status_code == 422
