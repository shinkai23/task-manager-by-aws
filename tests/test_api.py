from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_user(username: str, email: str, password: str = "password123"):
    response = client.post(
        "/users/",
        json={"username": username, "email": email, "password": password},
    )
    assert response.status_code == 200, response.text
    return response.json()


def login(email: str, password: str = "password123"):
    response = client.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_user_registration_and_login():
    user = create_user("alice", "alice@example.com")

    assert user["username"] == "alice"
    assert user["email"] == "alice@example.com"
    assert "password" not in user

    headers = login("alice@example.com")
    response = client.get("/users/me", headers=headers)

    assert response.status_code == 200
    assert response.json()["email"] == "alice@example.com"


def test_duplicate_email_returns_bad_request():
    create_user("alice", "alice@example.com")

    response = client.post(
        "/users/",
        json={
            "username": "alice2",
            "email": "alice@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "BAD_REQUEST"


def test_task_crud_is_scoped_to_current_user():
    create_user("alice", "alice@example.com")
    create_user("bob", "bob@example.com")
    alice_headers = login("alice@example.com")
    bob_headers = login("bob@example.com")

    response = client.post(
        "/tasks/",
        json={
            "title": "Write tests",
            "description": "Cover auth and task scope",
            "status": "todo",
            "priority": "medium",
        },
        headers=alice_headers,
    )
    assert response.status_code == 200, response.text
    task = response.json()

    response = client.get("/tasks/", headers=alice_headers)
    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [task["id"]]

    response = client.get(f"/tasks/{task['id']}", headers=bob_headers)
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"

    response = client.put(
        f"/tasks/{task['id']}",
        json={"status": "done"},
        headers=alice_headers,
    )
    assert response.status_code == 200
    assert response.json()["status"] == "done"

    response = client.delete(f"/tasks/{task['id']}", headers=alice_headers)
    assert response.status_code == 200

    response = client.get("/tasks/", headers=alice_headers)
    assert response.status_code == 200
    assert response.json() == []


def test_invalid_login_returns_unauthorized():
    create_user("alice", "alice@example.com")

    response = client.post(
        "/auth/login",
        json={"email": "alice@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"
