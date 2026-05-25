import pytest


class TestNotFound:
    def test_get_nonexistent_product(self, client):
        resp = client.get("/products/999")
        assert resp.status_code == 404
        assert resp.json()["detail"] == "Product not found"

    def test_patch_select_nonexistent_product(self, client):
        resp = client.patch("/products/999/select", json={"selected": True})
        assert resp.status_code == 404

    def test_put_nonexistent_product(self, client):
        resp = client.put("/products/999", json={"name": "X", "price": 1, "stock": 1})
        assert resp.status_code == 404

    def test_nonexistent_route(self, client):
        resp = client.get("/nonexistent")
        assert resp.status_code == 404


class TestValidationErrors:
    def test_create_product_empty_body(self, client):
        resp = client.post("/products", json={})
        assert resp.status_code == 422

    def test_create_product_wrong_types(self, client):
        resp = client.post("/products", json={"name": 123, "price": "free", "stock": "lots"})
        assert resp.status_code == 422

    def test_create_order_missing_user_id(self, client):
        resp = client.post("/orders", json={"product_ids": [1], "quantity": 1})
        assert resp.status_code == 422

    def test_create_order_wrong_product_id_type(self, client):
        resp = client.post(
            "/orders",
            json={"user_id": 1, "product_ids": ["not-a-number"], "quantity": 1},
        )
        assert resp.status_code == 422

    def test_create_user_empty_body(self, client):
        resp = client.post("/users", json={})
        assert resp.status_code == 422

    def test_patch_select_missing_selected_field(self, client):
        resp = client.patch("/products/1/select", json={})
        assert resp.status_code == 422

    def test_patch_select_wrong_type(self, client):
        resp = client.patch("/products/1/select", json={"selected": "probably"})
        assert resp.status_code == 422


class TestIdempotency:
    def test_double_select_keeps_selected(self, client):
        client.patch("/products/1/select", json={"selected": True})
        client.patch("/products/1/select", json={"selected": True})
        resp = client.get("/products/1")
        assert resp.json()["selected"] is True

    def test_double_deselect_keeps_deselected(self, client):
        client.patch("/products/1/select", json={"selected": False})
        client.patch("/products/1/select", json={"selected": False})
        resp = client.get("/products/1")
        assert resp.json()["selected"] is False


class TestBoundaries:
    def test_negative_quantity(self, client):
        client.patch("/products/1/select", json={"selected": True})
        resp = client.post("/orders", json={"user_id": 1, "product_ids": [1], "quantity": -1})
        assert resp.status_code == 200

    def test_zero_quantity(self, client):
        client.patch("/products/1/select", json={"selected": True})
        resp = client.post("/orders", json={"user_id": 1, "product_ids": [1], "quantity": 0})
        assert resp.status_code == 200

    def test_negative_price(self, client):
        resp = client.post("/products", json={"name": "Free Money", "price": -100, "stock": 1})
        assert resp.status_code == 200


class TestMissingSelectedField:
    def test_new_product_missing_selected_key(self, client):
        resp = client.post("/products", json={"name": "New", "price": 10, "stock": 5})
        assert "selected" not in resp.json()

    @pytest.mark.xfail(strict=True, reason="Bug: new products lack 'selected' key, causing KeyError in POST /orders")
    def test_order_after_creating_product_does_not_crash(self, client):
        client.post("/products", json={"name": "New", "price": 10, "stock": 5})
        resp = client.post("/orders", json={"user_id": 1, "product_ids": [4], "quantity": 1})
        assert resp.status_code == 200
