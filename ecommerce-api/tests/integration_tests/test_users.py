class TestListUsers:
    def test_returns_empty_list_initially(self, client):
        resp = client.get("/users")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_includes_created_users(self, client):
        client.post("/users", json={"name": "Alice", "email": "alice@example.com"})
        resp = client.get("/users")
        assert len(resp.json()) == 1


class TestCreateUser:
    def test_creates_user(self, client):
        resp = client.post("/users", json={"name": "Alice", "email": "alice@example.com"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "Alice"
        assert data["email"] == "alice@example.com"
        assert data["id"] == 1

    def test_increments_id(self, client):
        client.post("/users", json={"name": "A", "email": "a@a.com"})
        resp = client.post("/users", json={"name": "B", "email": "b@b.com"})
        assert resp.json()["id"] == 2

    def test_missing_required_field_returns_422(self, client):
        resp = client.post("/users", json={"name": "NoEmail"})
        assert resp.status_code == 422
