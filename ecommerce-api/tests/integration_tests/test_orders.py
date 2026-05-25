from main import products_db


def _select_and_order(client, product_ids, selected_ids=None):
    if selected_ids is None:
        selected_ids = product_ids
    for pid in selected_ids:
        client.patch(f"/products/{pid}/select", json={"selected": True})
    return client.post("/orders", json={"user_id": 1, "product_ids": product_ids, "quantity": 1})


class TestCreateOrder:
    def test_creates_order_for_selected_product(self, client):
        client.patch("/products/1/select", json={"selected": True})
        resp = client.post("/orders", json={"user_id": 42, "product_ids": [1], "quantity": 2})
        assert resp.status_code == 200
        data = resp.json()
        assert data["user_id"] == 42
        assert data["product_ids"] == [1]
        assert data["quantity"] == 2
        assert data["status"] == "pending"
        assert "created_at" in data

    def test_filters_out_unselected_products(self, client):
        client.patch("/products/1/select", json={"selected": True})
        resp = client.post("/orders", json={"user_id": 1, "product_ids": [1, 2], "quantity": 1})
        assert resp.json()["product_ids"] == [1]

    def test_returns_empty_list_when_none_selected(self, client):
        resp = client.post("/orders", json={"user_id": 1, "product_ids": [1, 2, 3], "quantity": 1})
        assert resp.json()["product_ids"] == []

    def test_empty_product_ids(self, client):
        resp = client.post("/orders", json={"user_id": 1, "product_ids": [], "quantity": 1})
        assert resp.json()["product_ids"] == []

    def test_increments_order_id(self, client):
        client.patch("/products/1/select", json={"selected": True})
        r1 = client.post("/orders", json={"user_id": 1, "product_ids": [1], "quantity": 1})
        r2 = client.post("/orders", json={"user_id": 1, "product_ids": [1], "quantity": 1})
        assert r2.json()["id"] == r1.json()["id"] + 1


class TestListOrders:
    def test_returns_all_orders(self, client):
        resp = client.get("/orders")
        assert resp.status_code == 200
        assert len(resp.json()) == 1

    def test_includes_new_orders(self, client):
        client.patch("/products/1/select", json={"selected": True})
        client.post("/orders", json={"user_id": 1, "product_ids": [1], "quantity": 1})
        resp = client.get("/orders")
        assert len(resp.json()) == 2


class TestPurchaseFlow:
    def test_select_then_deselect_then_order_excludes_product(self, client):
        client.patch("/products/1/select", json={"selected": True})
        client.patch("/products/1/select", json={"selected": False})
        resp = client.post("/orders", json={"user_id": 1, "product_ids": [1], "quantity": 1})
        assert resp.json()["product_ids"] == []

    def test_select_then_order_sequential_works_correctly(self, client):
        client.patch("/products/1/select", json={"selected": True})
        client.patch("/products/2/select", json={"selected": True})
        resp = client.post("/orders", json={"user_id": 1, "product_ids": [1, 2, 3], "quantity": 1})
        assert resp.json()["product_ids"] == [1, 2]

    def test_quantity_defaults(self, client):
        client.patch("/products/1/select", json={"selected": True})
        resp = client.post("/orders", json={"user_id": 1, "product_ids": [1]})
        assert resp.json()["quantity"] == 1
