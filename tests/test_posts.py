def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_post_lifecycle(client):
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
    response = client.post("/api/v1/posts", json={"title": "", "content": "body"})

    assert response.status_code == 422


def test_post_update_rejects_null(client):
    response = client.patch("/api/v1/posts/1", json={"title": None})

    assert response.status_code == 422
