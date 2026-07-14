from fastapi import FastAPI

app = FastAPI()

# --- Q1: Added 3 More Products (IDs 5, 6, 7) ---
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 599, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},
    {"id": 4, "name": "Desk Lamp", "price": 899, "category": "Electronics", "in_stock": False},
    {"id": 5, "name": "Laptop Stand", "price": 1299, "category": "Electronics", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 1899, "category": "Electronics", "in_stock": False}
]

# Base endpoint to check Q1 output
@app.get("/products")
def get_all_products():
    return {"products": products, "total": len(products)}

# --- Q2: Add a Category Filter Endpoint ---
@app.get("/products/category/{category_name}")
def get_by_category(category_name: str):
    result = [p for p in products if p["category"].lower() == category_name.lower()]
    if not result:
        return {"error": "No products found in this category"}
    return {"category": category_name, "products": result, "total": len(result)}

# --- Q3: Show Only In-Stock Products ---
@app.get("/products/instock")
def get_instock():
    available = [p for p in products if p["in_stock"] == True]
    return {"in_stock_products": available, "count": len(available)}

# --- Q4: Build a Store Info Endpoint ---
@app.get("/store/summary")
def store_summary():
    in_stock_count = len([p for p in products if p["in_stock"]])
    out_stock_count = len(products) - in_stock_count
    categories = list(set([p["category"] for p in products]))
    return {
        "store_name": "My E-commerce Store",
        "total_products": len(products),
        "in_stock": in_stock_count,
        "out_of_stock": out_stock_count,
        "categories": categories,
    }

# --- Q5: Search Products by Name (Case-Insensitive) ---
@app.get("/products/search/{keyword}")
def search_products(keyword: str):
    results = [
        p for p in products
        if keyword.lower() in p["name"].lower()
    ]
    if not results:
        return {"message": "No products matched your search"}
    return {"keyword": keyword, "results": results, "total_matches": len(results)}

# --- BONUS: Cheapest & Most Expensive Product ---
@app.get("/products/deals")
def get_deals():
    cheapest = min(products, key=lambda p: p["price"])
    expensive = max(products, key=lambda p: p["price"])
    return {
        "best_deal": cheapest,
        "premium_pick": expensive,
    }
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()

# --- THE MASTER DATABASE ---
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},
    {"id": 4, "name": "Desk Lamp", "price": 899, "category": "Electronics", "in_stock": False},
    {"id": 5, "name": "Laptop Stand", "price": 1299, "category": "Electronics", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 1899, "category": "Electronics", "in_stock": False},
    {"id": 8, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False} # Added for Day 2 tests
]

orders = []
feedback = []

# ==========================================
#         DAY 1 ENDPOINTS (GET ONLY)
# ==========================================

@app.get("/products")
def get_all_products():
    return {"products": products, "total": len(products)}

@app.get("/products/category/{category_name}")
def get_by_category(category_name: str):
    result = [p for p in products if p["category"].lower() == category_name.lower()]
    if not result:
        return {"error": "No products found in this category"}
    return {"category": category_name, "products": result, "total": len(result)}

@app.get("/products/instock")
def get_instock():
    available = [p for p in products if p["in_stock"] == True]
    return {"in_stock_products": available, "count": len(available)}

@app.get("/store/summary")
def store_summary():
    in_stock_count = len([p for p in products if p["in_stock"]])
    out_stock_count = len(products) - in_stock_count
    categories = list(set([p["category"] for p in products]))
    return {
        "store_name": "My E-commerce Store",
        "total_products": len(products),
        "in_stock": in_stock_count,
        "out_of_stock": out_stock_count,
        "categories": categories,
    }

@app.get("/products/search/{keyword}")
def search_products(keyword: str):
    results = [p for p in products if keyword.lower() in p["name"].lower()]
    if not results:
        return {"message": "No products matched your search"}
    return {"keyword": keyword, "results": results, "total_matches": len(results)}

@app.get("/products/deals")
def get_deals_day1():
    cheapest = min(products, key=lambda p: p["price"])
    expensive = max(products, key=lambda p: p["price"])
    return {"best_deal": cheapest, "premium_pick": expensive}

# ==========================================
#   DAY 2 ENDPOINTS (POST, PYDANTIC, QUERY)
# ==========================================

# --- Q1: Filter Products by Minimum Price ---
@app.get("/products/filter")
def filter_products(
    category: Optional[str] = None,
    max_price: Optional[int] = None,
    min_price: int = Query(None, description='Minimum price') #[cite: 8]
):
    result = products
    if category:
        result = [p for p in result if p["category"].lower() == category.lower()]
    if max_price:
        result = [p for p in result if p["price"] <= max_price]
    if min_price:
        result = [p for p in result if p["price"] >= min_price] #[cite: 8]
    return result

# --- Q2: Get Only the Price of a Product ---
@app.get("/products/{product_id}/price") #[cite: 8]
def get_product_price(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return {"name": product["name"], "price": product["price"]} #[cite: 8]
    return {"error": "Product not found"} #[cite: 8]

# --- Q3: Accept Customer Feedback ---
class CustomerFeedback(BaseModel): #[cite: 8]
    customer_name: str = Field(..., min_length=2, max_length=100) #[cite: 8]
    product_id: int = Field(..., gt=0) #[cite: 8]
    rating: int = Field(..., ge=1, le=5) #[cite: 8]
    comment: Optional[str] = Field(None, max_length=300) #[cite: 8]

@app.post("/feedback") #[cite: 8]
def submit_feedback(data: CustomerFeedback): #[cite: 8]
    feedback.append(data.dict()) #[cite: 8]
    return {
        "message": "Feedback submitted successfully", #[cite: 8]
        "feedback": data.dict(), #[cite: 8]
        "total_feedback": len(feedback), #[cite: 8]
    }

# --- Q4: Build a Product Summary Dashboard ---
@app.get("/products/summary") #[cite: 8]
def product_summary():
    in_stock = [p for p in products if p["in_stock"]] #[cite: 8]
    out_stock = [p for p in products if not p["in_stock"]] #[cite: 8]
    expensive = max(products, key=lambda p: p["price"]) #[cite: 8]
    cheapest = min(products, key=lambda p: p["price"]) #[cite: 8]
    categories = list(set(p["category"] for p in products)) #[cite: 8]
    return {
        "total_products": len(products), #[cite: 8]
        "in_stock_count": len(in_stock), #[cite: 8]
        "out_of_stock_count": len(out_stock), #[cite: 8]
        "most_expensive": {"name": expensive["name"], "price": expensive["price"]}, #[cite: 8]
        "cheapest": {"name": cheapest["name"], "price": cheapest["price"]}, #[cite: 8]
        "categories": categories, #[cite: 8]
    }

# --- Q5: Validate & Place a Bulk Order ---
class OrderItem(BaseModel): #[cite: 8]
    product_id: int = Field(..., gt=0) #[cite: 8]
    quantity: int = Field(..., gt=0, le=50) #[cite: 8]

class BulkOrder(BaseModel): #[cite: 8]
    company_name: str = Field(..., min_length=2) #[cite: 8]
    contact_email: str = Field(..., min_length=5) #[cite: 8]
    items: List[OrderItem] = Field(..., min_items=1) #[cite: 8]

@app.post("/orders/bulk") #[cite: 8]
def place_bulk_order(order: BulkOrder):
    confirmed, failed, grand_total = [], [], 0 #[cite: 8]
    for item in order.items: #[cite: 8]
        product = next((p for p in products if p["id"] == item.product_id), None) #[cite: 8]
        if not product:
            failed.append({"product_id": item.product_id, "reason": "Product not found"}) #[cite: 8]
        elif not product["in_stock"]:
            failed.append({"product_id": item.product_id, "reason": f"{product['name']} is out of stock"}) #[cite: 8]
        else:
            subtotal = product["price"] * item.quantity #[cite: 8]
            grand_total += subtotal #[cite: 8]
            confirmed.append({"product": product["name"], "qty": item.quantity, "subtotal": subtotal}) #[cite: 8]
    return {
        "company": order.company_name, 
        "confirmed": confirmed, #[cite: 8]
        "failed": failed, #[cite: 8]
        "grand_total": grand_total #[cite: 8]
    }

# --- BONUS: Order Status Tracker ---
class SimpleOrder(BaseModel):
    product_id: int
    quantity: int

@app.post("/orders") #[cite: 8]
def place_order(order: SimpleOrder):
    new_order = {
        "order_id": len(orders) + 1,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "status": "pending" #[cite: 8]
    }
    orders.append(new_order)
    return new_order

@app.get("/orders/{order_id}") #[cite: 8]
def get_order(order_id: int):
    for order in orders: #[cite: 8]
        if order["order_id"] == order_id: #[cite: 8]
            return {"order": order} #[cite: 8]
    return {"error": "Order not found"} #[cite: 8]

@app.patch("/orders/{order_id}/confirm") #[cite: 8]
def confirm_order(order_id: int):
    for order in orders: #[cite: 8]
        if order["order_id"] == order_id: #[cite: 8]
            order["status"] = "confirmed" #[cite: 8]
            return {"message": "Order confirmed", "order": order} #[cite: 8]
    return {"error": "Order not found"} #[cite: 8]