import copy
import pytest
from fastapi.testclient import TestClient

from main import app, products_db, orders_db, users_db


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    saved = {
        "products": copy.deepcopy(products_db),
        "orders": copy.deepcopy(orders_db),
        "users": copy.deepcopy(users_db),
    }
    yield
    products_db[:] = saved["products"]
    orders_db[:] = saved["orders"]
    users_db[:] = saved["users"]
