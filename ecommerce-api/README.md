# E-Commerce API

A simple e-commerce API built with FastAPI, intended for API testing purposes.

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (package manager)

## Setup

```sh
uv sync --extra dev
```

This creates a virtual environment (`.venv`) and installs the project dependencies plus dev dependencies (pytest).

## Run the server locally

```sh
uv run uvicorn main:app --reload
```

The API will be available at:

- API: <http://127.0.0.1:8000>
- Interactive docs (Swagger UI): <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>
- Health check: <http://127.0.0.1:8000/internal/health>

## Run the tests

```sh
uv run pytest
```

## API overview

| Method | Path                       | Description                          |
| ------ | -------------------------- | ------------------------------------ |
| GET    | `/products`                | List all products                    |
| GET    | `/products/{id}`           | Get a product by ID                  |
| POST   | `/products`                | Create a product                     |
| PATCH  | `/products/{id}/select`    | Select/deselect a product            |
| GET    | `/orders`                  | List all orders                      |
| POST   | `/orders`                  | Create an order                      |
| GET    | `/users`                   | List all users                       |
| POST   | `/users`                   | Create a user                        |
| GET    | `/admin/stats`             | Basic internal stats                 |
| GET    | `/debug/db`                | Debug endpoint, full DB state        |
| GET    | `/internal/health`         | Health check                         |

Data is stored in memory and resets when the server restarts.
