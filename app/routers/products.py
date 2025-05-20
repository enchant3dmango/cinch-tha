from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import get_product_detail
from app.schemas import ProductDetail

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/products/{product_id}", response_model=ProductDetail)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product_detail(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found!")
    return product
