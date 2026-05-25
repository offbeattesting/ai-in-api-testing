from main import products_db


class TestListProducts:
    def test_returns_seed_data(self, client):
        resp = client.get("/products")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 3
        assert data[0]["name"] == "Laptop"

    def test_each_product_has_expected_fields(self, client):
        resp = client.get("/products")
        for p in resp.json():
            assert set(p.keys()) == {"id", "name", "price", "stock", "selected"}


class TestGetProduct:
    def test_by_id(self, client):
        resp = client.get("/products/1")
        assert resp.status_code == 200
        assert resp.json()["name"] == "Laptop"

    def test_not_found(self, client):
        resp = client.get("/products/999")
        assert resp.status_code == 404
        assert resp.json()["detail"] == "Product not found"


class TestCreateProduct:
    def test_creates_new_product(self, client):
        resp = client.post("/products", json={"name": "Tablet", "price": 499.99, "stock": 30})
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == 4
        assert data["name"] == "Tablet"

    def test_increments_id(self, client):
        client.post("/products", json={"name": "A", "price": 1, "stock": 1})
        client.post("/products", json={"name": "B", "price": 2, "stock": 2})
        resp = client.post("/products", json={"name": "C", "price": 3, "stock": 3})
        assert resp.json()["id"] == 6

    def test_missing_optional_fields_default(self, client):
        resp = client.post("/products", json={"name": "Test", "price": 10.0})
        assert resp.status_code == 200
        assert resp.json()["stock"] == 0

    def test_missing_required_field_returns_422(self, client):
        resp = client.post("/products", json={"name": "NoPrice"})
        assert resp.status_code == 422


class TestUpdateProduct:
    def test_updates_product(self, client):
        resp = client.put("/products/1", json={"name": "Gaming Laptop", "price": 1499.99, "stock": 25})
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "Gaming Laptop"
        assert data["price"] == 1499.99
        assert data["stock"] == 25

    def test_not_found(self, client):
        resp = client.put("/products/999", json={"name": "X", "price": 1, "stock": 1})
        assert resp.status_code == 404

    def test_does_not_reset_selected(self, client):
        client.patch("/products/1/select", json={"selected": True})
        client.put("/products/1", json={"name": "Laptop Pro", "price": 1299.99, "stock": 40})
        assert products_db[0]["selected"] is True


class TestSelectProduct:
    def test_select(self, client):
        resp = client.patch("/products/1/select", json={"selected": True})
        assert resp.status_code == 200
        assert resp.json()["selected"] is True

    def test_deselect(self, client):
        client.patch("/products/1/select", json={"selected": True})
        resp = client.patch("/products/1/select", json={"selected": False})
        assert resp.json()["selected"] is False

    def test_not_found(self, client):
        resp = client.patch("/products/999/select", json={"selected": True})
        assert resp.status_code == 404
