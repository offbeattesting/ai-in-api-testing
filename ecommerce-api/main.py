from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

app = FastAPI(
    title="E-Commerce API",
    description="A simple e-commerce API for testing purposes",
    version="1.0.0"
)

products_db = [
    {"id": 1, "name": "Laptop", "price": 999.99, "stock": 50},
    {"id": 2, "name": "Headphones", "price": 149.99, "stock": 200},
    {"id": 3, "name": "Keyboard", "price": 79.99, "stock": 150},
]

orders_db = []
users_db = []

class Product(BaseModel):
    name: str
    price: float
    stock: int = 0

class Order(BaseModel):
    user_id: int
    product_ids: list[int]
    quantity: int = 1

class User(BaseModel):
    name: str
    email: str

@app.get("/products", tags=["Products"])
async def get_products():
    """Get all available products"""
    return products_db

@app.get("/products/{product_id}", tags=["Products"])
async def get_product(product_id: int):
    """Get a specific product by ID"""
    for product in products_db:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/products", tags=["Products"])
async def create_product(product: Product):
    """Create a new product"""
    new_id = max(p["id"] for p in products_db) + 1
    new_product = {"id": new_id, **product.model_dump()}
    products_db.append(new_product)
    return new_product

@app.put("/products/{product_id}")
async def update_product(product_id: int, product: Product):
    for p in products_db:
        if p["id"] == product_id:
            p["name"] = product.name
            p["price"] = product.price
            p["stock"] = product.stock
            return p
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/orders", tags=["Orders"])
async def get_orders():
    """Get all orders"""
    return orders_db

@app.post("/orders", tags=["Orders"])
async def create_order(order: Order):
    """Create a new order"""
    new_id = len(orders_db) + 1
    new_order = {
        "id": new_id,
        "user_id": order.user_id,
        "product_ids": order.product_ids,
        "quantity": order.quantity,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    orders_db.append(new_order)
    return new_order

@app.get("/users", tags=["Users"])
async def get_users():
    """Get all users"""
    return users_db

@app.post("/users", tags=["Users"])
async def create_user(user: User):
    """Create a new user"""
    new_id = len(users_db) + 1
    new_user = {"id": new_id, **user.model_dump()}
    users_db.append(new_user)
    return new_user

@app.get("/admin/stats")
async def get_stats():
    """Get basic stats (internal use only)"""
    return {
        "total_products": len(products_db),
        "total_orders": len(orders_db),
        "total_users": len(users_db)
    }

@app.get("/debug/db")
async def debug_db():
    """Debug endpoint - exposes full database state"""
    return {
        "products": products_db,
        "orders": orders_db,
        "users": users_db
    }

@app.get("/internal/health")
async def health_check():
    """Internal health check endpoint"""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}
