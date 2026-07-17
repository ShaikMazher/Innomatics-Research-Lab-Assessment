from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

# --- Initial Database ---
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True}
]

# Temporary memory for the session
cart = []
orders = []

class CheckoutRequest(BaseModel):
    customer_name: str
    delivery_address: str

def find_product(product_id: int):
    return next((p for p in products if p["id"] == product_id), None)

def calculate_total(product, quantity):
    return product["price"] * quantity

# --- Cart Endpoints ---

@app.get("/cart")
def view_cart():
    if not cart:
        return {"message": "Cart is empty", "items": [], "item_count": 0, "grand_total": 0}
    
    grand_total = sum(item["subtotal"] for item in cart)
    return {
        "items": cart,
        "item_count": len(cart),
        "grand_total": grand_total
    }

@app.post("/cart/add")
def add_to_cart(product_id: int, quantity: int = 1):
    product = find_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if not product["in_stock"]:
        raise HTTPException(status_code=400, detail=f"{product['name']} is out of stock")

    # Q4 Logic: If item already exists in cart, update quantity
    for item in cart:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            item["subtotal"] = calculate_total(product, item["quantity"])
            return {"message": "Cart updated", "cart_item": item}

    # Q1 Logic: New item added to cart
    new_item = {
        "product_id": product_id,
        "product_name": product["name"],
        "quantity": quantity,
        "unit_price": product["price"],
        "subtotal": calculate_total(product, quantity)
    }
    cart.append(new_item)
    return {"message": "Added to cart", "cart_item": new_item}

@app.delete("/cart/{product_id}")
def remove_from_cart(product_id: int):
    global cart
    for item in cart:
        if item["product_id"] == product_id:
            cart.remove(item)
            return {"message": f"{item['product_name']} removed from cart"}
    raise HTTPException(status_code=404, detail="Product not in cart")

@app.post("/cart/checkout")
def checkout(details: CheckoutRequest):
    global cart
    
    # BONUS Logic: Empty Cart Check
    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty — add items first")

    grand_total = sum(item["subtotal"] for item in cart)
    placed_orders = []
    
    for item in cart:
        new_order = {
            "order_id": len(orders) + 1,
            "customer_name": details.customer_name,
            "delivery_address": details.delivery_address,
            "product": item["product_name"],
            "quantity": item["quantity"],
            "total_price": item["subtotal"]
        }
        orders.append(new_order)
        placed_orders.append(new_order)

    cart.clear() # Empty the cart after successful checkout
    
    return {
        "message": "Checkout successful",
        "orders_placed": len(placed_orders),
        "grand_total": grand_total,
        "details": placed_orders
    }

@app.get("/orders")
def get_orders():
    return {"orders": orders, "total_orders": len(orders)}