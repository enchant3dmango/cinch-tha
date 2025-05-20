from sqlalchemy.orm import Session, joinedload
from collections import defaultdict
from app import models


def get_product_detail(db: Session, product_id: int):
    product = db.query(models.Product).options(
        joinedload(models.Product.attributes).joinedload(models.Attribute.values),
        joinedload(models.Product.pricing).joinedload(models.ProductPricing.region),
        joinedload(models.Product.pricing).joinedload(models.ProductPricing.rental_period)
    ).filter(models.Product.id == product_id).first()

    if not product:
        return None

    # Group attribute values under their attribute
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
