from collections import defaultdict
from typing import Optional

from sqlalchemy.orm import Session, joinedload

from app import models


def get_product_detail(
    db: Session,
    product_id: int,
    attribute_limit: int = 10,
    attribute_offset: int = 0,
    pricing_limit: int = 10,
    pricing_offset: int = 0
):
    product = db.query(models.Product).options(
        joinedload(models.Product.attributes).joinedload(models.Attribute.values),
        joinedload(models.Product.pricing).joinedload(models.ProductPricing.region),
        joinedload(models.Product.pricing).joinedload(models.ProductPricing.rental_period)
    ).filter(models.Product.id == product_id).first()

    if not product:
        return None

    # Paginated attributes
    paginated_attributes = product.attributes[
        attribute_offset:attribute_offset + attribute_limit
    ]

    attribute_map = defaultdict(list)
    attribute_values_map = defaultdict(list)

    for a in paginated_attributes:
        for av in a.values:
            attribute_values_map[a.id].append({
                "id": av.id,
                "value": av.value
            })
        attribute_map[a.id] = a.name

    attributes = [
        {
            "id": attribute_id,
            "name": attribute_map[attribute_id],
            "values": attribute_values_map[attribute_id]
        }
        for attribute_id in attribute_map
    ]

    # Paginated pricing
    paginated_pricing = product.pricing[pricing_offset: pricing_offset + pricing_limit]

    pricing = [
        {
            "region": price.region.name,
            "rental_period": price.rental_period.duration_in_months,
            "final_price": price.final_price
        }
        for price in paginated_pricing
    ]

    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "sku": product.sku,
        "base_price": product.base_price,
        "attributes": attributes,
        "pricing": pricing
    }


def get_filtered_products(
    db: Session,
    region: Optional[str] = None,
    rental_months: Optional[int] = None
):
    query = db.query(models.Product).options(
        joinedload(models.Product.attributes).joinedload(models.Attribute.values),
        joinedload(models.Product.pricing).joinedload(models.ProductPricing.region),
        joinedload(models.Product.pricing).joinedload(models.ProductPricing.rental_period)
    )

    if region or rental_months:
        query = query.join(models.Product.pricing)

        if region:
            query = query.join(models.ProductPricing.region).filter(
                models.Region.name == region)
        if rental_months:
            query = query.join(models.ProductPricing.rental_period).filter(
                models.RentalPeriod.duration_in_months == rental_months
            )

    products = query.all()

    result = []
    for product in products:
        attribute_map = defaultdict(list)
        attribute_values_map = defaultdict(list)

        for a in product.attributes:
            for av in a.values:
                attribute_values_map[a.id].append({
                    "id": av.id,
                    "value": av.value
                })
            attribute_map[a.id] = a.name

        attributes = [
            {
                "id": attribute_id,
                "name": attribute_map[attribute_id],
                "values": attribute_values_map[attribute_id]
            }
            for attribute_id in attribute_map
        ]

        pricing = [
            {
                "region": price.region.name,
                "rental_period": price.rental_period.duration_in_months,
                "final_price": price.final_price
            }
            for price in product.pricing
            if (not region or price.region.name == region)
            and (not rental_months or price.rental_period.duration_in_months == rental_months)
        ]

        result.append({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "sku": product.sku,
            "base_price": product.base_price,
            "attributes": attributes,
            "pricing": pricing
        })

    return result
