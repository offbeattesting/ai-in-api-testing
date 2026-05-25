class TestHealth:
    def test_health_returns_ok(self, client):
        resp = client.get("/internal/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "timestamp" in data


class TestStats:
    def test_stats_returns_counts(self, client):
        resp = client.get("/admin/stats")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_products"] == 3
        assert data["total_orders"] == 1
        assert data["total_users"] == 0

    def test_stats_updates_after_creation(self, client):
        client.post("/users", json={"name": "A", "email": "a@a.com"})
        resp = client.get("/admin/stats")
        assert resp.json()["total_users"] == 1


class TestDebugDb:
    def test_debug_returns_full_state(self, client):
        resp = client.get("/debug/db")
        assert resp.status_code == 200
        data = resp.json()
        assert "products" in data
        assert "orders" in data
        assert "users" in data
        assert len(data["products"]) == 3
        assert len(data["orders"]) == 1
        assert len(data["users"]) == 0


class TestPurchases:
    def test_purchases_returns_orders_by_customer_id(self, client):
        resp = client.get("/purchases?user_id=12345")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["customer_id"] == 12345

    def test_purchases_returns_empty_for_unknown_user(self, client):
        resp = client.get("/purchases?user_id=99999")
        assert resp.status_code == 200
        assert resp.json() == []
