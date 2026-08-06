import httpx
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

# ECOMMERCE_API = "https://ecommerce-api.fastapicloud.dev"
ECOMMERCE_API = "https://de4a2ab1-37e5-4b92-814c-4a82589cd214.mock.pstmn.io"

ORDER_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Shopping Cart</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f5f5f5; display: flex; justify-content: center; padding: 40px 20px; }}
    .cart {{ background: #fff; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); width: 100%; max-width: 520px; padding: 40px; }}
    h1 {{ font-size: 24px; margin-bottom: 32px; }}
    .items {{ list-style: none; display: flex; flex-direction: column; gap: 16px; margin-bottom: 32px; }}
    .item {{ display: flex; align-items: center; gap: 16px; padding: 18px; background: #fafafa; border-radius: 8px; border: 1px solid #eee; }}
    .item-icon {{ font-size: 28px; width: 44px; height: 44px; display: flex; align-items: center; justify-content: center; background: #fff; border-radius: 8px; border: 1px solid #e0e0e0; flex-shrink: 0; }}
    .item-details {{ flex: 1; }}
    .item-name {{ font-weight: 600; font-size: 15px; }}
    .item-price {{ color: #666; font-size: 14px; margin-top: 2px; }}
    .item-qty {{ font-size: 13px; color: #999; }}
    .cart-total {{ display: flex; justify-content: space-between; font-size: 18px; font-weight: 700; padding-top: 24px; border-top: 2px solid #eee; margin-bottom: 28px; }}
    button {{ width: 100%; padding: 16px; background: #2563eb; color: #fff; border: none; border-radius: 8px; font-size: 16px; font-weight: 600; cursor: pointer; transition: background 0.15s; }}
    button:hover {{ background: #1d4ed8; }}
    .error {{ background: #fef2f2; color: #b91c1c; padding: 14px 18px; border-radius: 8px; margin-bottom: 24px; font-size: 14px; border: 1px solid #fecaca; }}
  </style>
</head>
<body>
  <div class="cart">
    <h1>Shopping Cart</h1>
    {error_html}
    <ul class="items">
      <li class="item">
        <div class="item-icon">👟</div>
        <div class="item-details">
          <div class="item-name">Shoes</div>
          <div class="item-price">$89.99</div>
        </div>
        <div class="item-qty">Qty: 1</div>
      </li>
      <li class="item">
        <div class="item-icon">👕</div>
        <div class="item-details">
          <div class="item-name">T-Shirt</div>
          <div class="item-price">$29.99</div>
        </div>
        <div class="item-qty">Qty: 2</div>
      </li>
    </ul>
    <div class="cart-total">
      <span>Total</span>
      <span>$149.97</span>
    </div>
    <form action="/place-order" method="post">
      <button type="submit">Place Order</button>
    </form>
  </div>
</body>
</html>"""

PAYMENT_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Payment</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f5f5f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 40px 20px; }}
    .card {{ background: #fff; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); width: 100%; max-width: 440px; padding: 40px; }}
    h1 {{ font-size: 24px; margin-bottom: 32px; }}
    form {{ display: flex; flex-direction: column; gap: 28px; }}
    form > * {{ flex-grow: 1; }}
    label {{ display: block; font-size: 14px; font-weight: 600; color: #333; margin-bottom: 8px; }}
    input {{ width: 100%; padding: 14px 16px; border: 1px solid #d1d5db; border-radius: 8px; font-size: 15px; outline: none; transition: border-color 0.15s; }}
    input:focus {{ border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,0.1); }}
    .row {{ display: flex; gap: 20px; }}
    .row .field {{ flex: 1; }}
    button {{ width: 100%; padding: 16px; background: #2563eb; color: #fff; border: none; border-radius: 8px; font-size: 16px; font-weight: 600; cursor: pointer; transition: background 0.15s; }}
    button:hover {{ background: #1d4ed8; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>Payment</h1>
    <form>
      <div class="field">
        <label for="card-number">Card Number</label>
        <input type="text" id="card-number" name="card_number" placeholder="1234 5678 9012 3456">
      </div>
      <div class="row">
        <div class="field">
          <label for="expiry">Expiry Date</label>
          <input type="text" id="expiry" name="expiry" placeholder="MM/YY">
        </div>
        <div class="field">
          <label for="cvv">CVV</label>
          <input type="text" id="cvv" name="cvv" placeholder="123">
        </div>
      </div>
      <button type="submit">Pay</button>
    </form>
  </div>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
async def order_page(error: str = None):
    error_html = f'<div class="error">{error}</div>' if error else ""
    return ORDER_PAGE.format(error_html=error_html)


@app.post("/place-order")
async def place_order():
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{ECOMMERCE_API}/orders",
            json={"user_id": 1, "product_ids": [1, 2], "quantities": [1, 2]},
        )
        print(resp.text)
    if resp.is_success:
        return RedirectResponse(url="/payment", status_code=302)
    return RedirectResponse(url="/?error=Placing+the+order+failed", status_code=302)


@app.get("/payment", response_class=HTMLResponse)
async def payment_page():
    return PAYMENT_PAGE
