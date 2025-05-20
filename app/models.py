from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class AuditMixin:
    created_at = Column(DateTime, nullable=False, default=func.now())
    created_by = Column(String(255))
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    updated_by = Column(String(255))
    is_deleted = Column(Integer, default=0)


class Product(Base, AuditMixin):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    sku = Column(String(255), nullable=False)
    base_price = Column(Float, nullable=False)

    attributes = relationship("Attribute", back_populates="product")
    pricing = relationship("ProductPricing", back_populates="product")


class Attribute(Base, AuditMixin):
    __tablename__ = "attributes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    product = relationship("Product", back_populates="attributes")
    values = relationship("AttributeValue", back_populates="attribute")


class AttributeValue(Base, AuditMixin):
    __tablename__ = "attribute_values"
    id = Column(Integer, primary_key=True, index=True)
    value = Column(String(255), nullable=False)

    attribute_id = Column(Integer, ForeignKey("attributes.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    attribute = relationship("Attribute", back_populates="values")


class RentalPeriod(Base, AuditMixin):
    __tablename__ = "rental_periods"
    id = Column(Integer, primary_key=True, index=True)
    duration_in_months = Column(Integer, nullable=False)
    multiplier = Column(Float, nullable=False)

    pricing = relationship("ProductPricing", back_populates="rental_period")


class Region(Base, AuditMixin):
    __tablename__ = "regions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    fee = Column(Float, nullable=False)

    pricing = relationship("ProductPricing", back_populates="region")


class ProductPricing(Base, AuditMixin):
    __tablename__ = "product_pricing"
    id = Column(Integer, primary_key=True, index=True)
    final_price = Column(Float, nullable=False)

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    rental_period_id = Column(Integer, ForeignKey("rental_periods.id"), nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)

    product = relationship("Product", back_populates="pricing")
    rental_period = relationship("RentalPeriod", back_populates="pricing")
    region = relationship("Region", back_populates="pricing")
