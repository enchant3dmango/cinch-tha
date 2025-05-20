# tests/test_products.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import Product, ProductPricing, Region, RentalPeriod

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(bind=engine)

# Create fresh schema
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture
def test_data():
    db = TestingSessionLocal()

    # Create minimal test data
    region = Region(name="Singapore", fee=10)
    rental_period = RentalPeriod(duration_in_months=3, multiplier=1.2)
    product = Product(
        name="Salomon X Ultra 360",
        description="Great hiking shoes.",
        sku="X1",
        base_price=100.0
    )
    pricing = ProductPricing(
        product=product,
        rental_period=rental_period,
        region=region,
        final_price=99.0
    )

    db.add_all([region, rental_period, product, pricing])
    db.flush()

    pricing = ProductPricing(
        product_id=product.id,
        region_id=region.id,
        rental_period_id=rental_period.id,
        final_price=110.0
    )
    db.add(pricing)
    db.commit()
    db.close()


def test_read_product(test_data):
    response = client.get("/products/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Salomon X Ultra 360"
    assert "pricing" in data


def test_read_product_not_found():
    response = client.get("/products/999")
    assert response.status_code == 404


def test_list_products_all(test_data):
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_filter_by_region(test_data):
    response = client.get("/products?region=Singapore")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_filter_by_rental_months(test_data):
    response = client.get("/products?rental_months=3")
    assert response.status_code == 200
    assert len(response.json()) > 0
