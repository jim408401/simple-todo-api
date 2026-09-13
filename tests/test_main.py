import pytest

from app.main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "ok"


def test_get_todos(client):
    response = client.get("/todos")

    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_get_existing_todo(client):
    response = client.get("/todos/1")

    assert response.status_code == 200
    assert response.json["id"] == 1


def test_get_non_existing_todo(client):
    response = client.get("/todos/9999")

    assert response.status_code == 404


def test_create_todo(client):
    response = client.post(
        "/todos",
        json={
            "title": "Write Jenkins Pipeline"
        }
    )

    assert response.status_code == 201
    assert response.json["title"] == "Write Jenkins Pipeline"


def test_create_todo_without_title(client):
    response = client.post(
        "/todos",
        json={}
    )

    assert response.status_code == 400


def test_update_todo(client):
    response = client.put(
        "/todos/1",
        json={
            "done": True
        }
    )

    assert response.status_code == 200
    assert response.json["done"] is True


def test_delete_todo(client):
    response = client.delete("/todos/1")

    assert response.status_code == 200
