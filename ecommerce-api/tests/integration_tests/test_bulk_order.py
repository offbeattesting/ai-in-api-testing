"""Create 100 one-cent products and place an order for all of them.

Usage:
    uv run pytest tests/integration_tests/test_bulk_order.py -v -s
"""
import sys
from fastapi.testclient import TestClient
from main import app


def bulk_create_and_order(client):
    product_ids = []

    for i in range(1, 101):
        resp = client.post("/products", json={
            "name": f"One Cent Product {i}",
            "price": 0.01,
            "stock": 1000,
        })
        assert resp.status_code == 200, f"Create product {i} failed: {resp.json()}"
        new_id = resp.json()["id"]
        product_ids.append(new_id)
        print(f"  Created product {new_id}: One Cent Product {i}")

    print(f"\nCreated {len(product_ids)} products")

    for pid in product_ids:
        resp = client.patch(f"/products/{pid}/select", json={"selected": True})
        assert resp.status_code == 200, f"Select product {pid} failed: {resp.json()}"
    print(f"Selected {len(product_ids)} products")

    quantities = [1] * len(product_ids)
    resp = client.post("/orders", json={
        "user_id": 42,
        "product_ids": product_ids,
        "quantities": quantities,
    })
    print(f"\nOrder response status: {resp.status_code}")
    result = resp.json()
    print(f"Order response body: {result}")
    return result


def test_bulk_order_of_100_products(client):
    result = bulk_create_and_order(client)
    assert "id" in result
    assert result["status"] == "pending"
    print("\nTest PASSED")


if __name__ == "__main__":
    client = TestClient(app)
    print("Running bulk order script (100 x 1-cent products)...\n")
    try:
        result = bulk_create_and_order(client)
        print(f"\nScript completed successfully. Order ID: {result.get('id')}")
    except Exception as e:
        print(f"\nScript FAILED: {e}")
        sys.exit(1)
