from fastapi import FastAPI, Query, Response, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# --- Initial Data ---
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True}
]

orders = [
    {"order_id": 1, "customer_name": "Rahul Sharma", "product": "Wireless Mouse", "quantity": 1},
    {"order_id": 2, "customer_name": "Priya Singh", "product": "Notebook", "quantity": 2},
    {"order_id": 3, "customer_name": "Rahul Kumar", "product": "USB Hub", "quantity": 1},
    {"order_id": 4, "customer_name": "Ananya Roy", "product": "Pen Set", "quantity": 5},
    {"order_id": 5, "customer_name": "Rahul Verma", "product": "Notebook", "quantity": 1}
]

# --- Q1: Search Products ---
@app.get('/products/search')
def search_products(keyword: str = Query(...)):
    results = [p for p in products if keyword.lower() in p['name'].lower()]
    if not results:
        return {'message': f'No products found for: {keyword}'}
    return {'keyword': keyword, 'total_found': len(results), 'products': results}

# --- Q2: Sort Products ---
@app.get('/products/sort')
def sort_products(sort_by: str = Query('price'), order: str = Query('asc')):
    if sort_by not in ['price', 'name']:
        return {'error': "sort_by must be 'price' or 'name'"}
    if order not in ['asc', 'desc']:
        return {'error': "order must be 'asc' or 'desc'"}
    
    reverse = (order == 'desc')
    results = sorted(products, key=lambda p: p[sort_by], reverse=reverse)
    return {'sort_by': sort_by, 'order': order, 'products': results}

# --- Q3: Paginate Products ---
@app.get('/products/page')
def paginate_products(page: int = Query(1, ge=1), limit: int = Query(2, ge=1)):
    start = (page - 1) * limit
    paged = products[start : start + limit]
    total_pages = -(-len(products) // limit)
    return {
        'page': page,
        'limit': limit,
        'total_products': len(products),
        'total_pages': total_pages,
        'products': paged
    }

# --- Q4: Search Orders ---
@app.get('/orders/search')
def search_orders(customer_name: str = Query(...)):
    results = [
        o for o in orders
        if customer_name.lower() in o['customer_name'].lower()
    ]
    if not results:
        return {'message': f'No orders found for: {customer_name}'}
    return {'customer_name': customer_name, 'total_found': len(results), 'orders': results}

# --- Q5: Sort Products by Category then Price ---
@app.get('/products/sort-by-category')
def sort_by_category():
    results = sorted(products, key=lambda p: (p['category'], p['price']))
    return {'products': results, 'total': len(results)}

# --- Q6: Search + Sort + Paginate (Browse) ---
@app.get('/products/browse')
def browse_products(
    keyword: Optional[str] = Query(None),
    sort_by: str = Query('price'),
    order: str = Query('asc'),
    page: int = Query(1, ge=1),
    limit: int = Query(4, ge=1, le=20),
):
    result = products
    if keyword:
        result = [p for p in result if keyword.lower() in p['name'].lower()]

    if sort_by in ['price', 'name']:
        result = sorted(result, key=lambda p: p[sort_by], reverse=(order == 'desc'))

    total = len(result)
    start = (page - 1) * limit
    paged = result[start : start + limit]

    return {
        'keyword': keyword, 
        'sort_by': sort_by, 
        'order': order,
        'page': page,  
        'limit': limit, 
        'total_found': total,
        'total_pages': -(-total // limit) if limit > 0 else 1,
        'products': paged,
    }

# --- BONUS: Paginate Orders ---
@app.get('/orders/page')
def get_orders_paged(
    page: int = Query(1, ge=1),
    limit: int = Query(3, ge=1, le=20),
):
    start = (page - 1) * limit
    return {
        'page': page,
        'limit': limit,
        'total': len(orders),
        'total_pages': -(-len(orders) // limit) if limit > 0 else 1,
        'orders': orders[start : start + limit],
    }

# --- Dynamic Route (Must stay at the bottom) ---
@app.get('/products/{product_id}')
def get_product_by_id(product_id: int, response: Response):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'error': 'Product not found'}
    return product