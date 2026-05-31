from fastapi import FastAPI
from faker import Faker
import random
from datetime import datetime

app = FastAPI(title="Sales Data API")

fake = Faker()

REGIONS = ["Europe", "North America", "Asia", "Africa"]
CATEGORIES = ["Electronics", "Clothing", "Home"]


def noisy(value, field_type):
    """Inject 20% noisy data for data quality testing"""
    if random.random() < 0.2:
        if field_type == "price":
            return -round(random.uniform(10, 500), 2)
        elif field_type == "quantity":
            return random.choice([-5, 0, 9999])
        elif field_type == "region":
            return "UNKNOWN_REGION"
        elif field_type == "date":
            return "invalid-date"
    return value


@app.get("/")
def root():
    return {
        "message": "Sales Data API running",
        "docs": "/docs"
    }


# ===================== PRODUCTS =====================
@app.get("/products")
def products(limit: int = 10):
    return [
        {
            "product_id": i,
            "product_name": fake.word(),
            "category": random.choice(CATEGORIES),
            "price": noisy(round(random.uniform(10, 500), 2), "price")
        }
        for i in range(1, limit + 1)
    ]


# ===================== CUSTOMERS =====================
@app.get("/customers")
def customers(limit: int = 10):
    return [
        {
            "customer_id": i,
            "name": fake.name(),
            "region": noisy(random.choice(REGIONS), "region")
        }
        for i in range(1, limit + 1)
    ]


# ===================== ORDERS =====================
@app.get("/orders")
def orders(limit: int = 20):
    return [
        {
            "order_id": i,
            "customer_id": random.randint(1, 20),
            "product_id": random.randint(1, 20),
            "quantity": noisy(random.randint(1, 10), "quantity"),
            "order_date": noisy(datetime.now().isoformat(), "date")
        }
        for i in range(1, limit + 1)
    ]
