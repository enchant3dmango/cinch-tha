from fastapi import APIRouter, Depends, HTTPException, Query
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
def read_product(
    product_id: int,
    db: Session = Depends(get_db),
    attribute_limit: int = Query(10, ge=0),
    attribute_offset: int = Query(0, ge=0),
    pricing_limit: int = Query(10, ge=0),
    pricing_offset: int = Query(0, ge=0)
):
    product = get_product_detail(
        db=db,
        product_id=product_id,
        attribute_limit=attribute_limit,
        attribute_offset=attribute_offset,
        pricing_limit=pricing_limit,
        pricing_offset=pricing_offset
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found!")
    return product
