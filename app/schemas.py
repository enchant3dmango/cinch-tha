from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class AuditMixin(BaseModel):
    created_at: datetime
    created_by: Optional[str]
    updated_at: datetime
    updated_by: Optional[str]
    is_deleted: int


class AttributeValueBase(BaseModel):
    value: str


class AttributeValueCreate(AttributeValueBase):
    attribute_id: int
    product_id: int


class AttributeValue(AttributeValueBase, AuditMixin):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AttributeBase(BaseModel):
    name: str


class AttributeCreate(AttributeBase):
    product_id: int


class Attribute(AttributeBase, AuditMixin):
    id: int
    values: List[AttributeValue] = []

    model_config = ConfigDict(from_attributes=True)


class RentalPeriodBase(BaseModel):
    duration_in_months: int
    multiplier: float


class RentalPeriodCreate(RentalPeriodBase):
    pass


class RentalPeriod(RentalPeriodBase, AuditMixin):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RegionBase(BaseModel):
    name: str
    fee: float


class RegionCreate(RegionBase):
    pass


class Region(RegionBase, AuditMixin):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ProductPricingBase(BaseModel):
    product_id: int
    rental_period_id: int
    region_id: int
    final_price: float


class ProductPricingCreate(ProductPricingBase):
    pass


class ProductPricing(ProductPricingBase, AuditMixin):
    id: int
    rental_period: RentalPeriod
    region: Region

    model_config = ConfigDict(from_attributes=True)


class ProductBase(BaseModel):
    name: str
    description: str
    sku: str
    base_price: float


class ProductCreate(ProductBase):
    pass


class Product(ProductBase, AuditMixin):
    id: int
    attributes: List[Attribute] = []
    pricing: List[ProductPricing] = []

    model_config = ConfigDict(from_attributes=True)


# Output schema for product detail
class AttributeValueOut(BaseModel):
    id: int
    value: str


class AttributeOut(BaseModel):
    id: int
    name: str
    values: List[AttributeValueOut]


class ProductPricingOut(BaseModel):
    region: str
    rental_period: int
    final_price: float


class ProductDetail(BaseModel):
    id: int
    name: str
    description: str
    sku: str
    base_price: float
    attributes: List[AttributeOut]
    pricing: List[ProductPricingOut]
