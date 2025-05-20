-- products
INSERT INTO products (name, description, sku, base_price, created_at, created_by, updated_at, updated_by, is_deleted)
VALUES ("Salomon X Ultra 360", "Great hiking shoes.", "X1", 500000.0,NOW(), "system", NOW(), "system", 0);

-- attributes
INSERT INTO attributes (name, product_id, created_at, created_by, updated_at, updated_by, is_deleted)
VALUES ("Size", 1, NOW(), "system", NOW(), "system", 0);
INSERT INTO attributes (name, product_id, created_at, created_by, updated_at, updated_by, is_deleted)
VALUES ("Color", 1, NOW(), "system", NOW(), "system", 0);

-- attribute_values
INSERT INTO attribute_values (value, product_id, attribute_id, created_at, created_by, updated_at, updated_by, is_deleted)
VALUES ("44", 1, 1, NOW(), "system", NOW(), "system", 0);
INSERT INTO attribute_values (value, product_id, attribute_id, created_at, created_by, updated_at, updated_by, is_deleted)
VALUES ("44.5", 1, 1, NOW(), "system", NOW(), "system", 0);
INSERT INTO attribute_values (value, product_id, attribute_id, created_at, created_by, updated_at, updated_by, is_deleted)
VALUES ("Black", 1, 2, NOW(), "system", NOW(), "system", 0);

-- region
INSERT INTO regions (name, fee, created_at, created_by, updated_at, updated_by, is_deleted)
VALUES ("Singapore", 20000, NOW(), "system", NOW(), "system", 0);
INSERT INTO regions (name, fee, created_at, created_by, updated_at, updated_by, is_deleted)
VALUES ("Malaysia", 25000, NOW(), "system", NOW(), "system", 0);

-- rental_periods
INSERT INTO rental_periods (duration_in_months, multiplier, created_at, created_by, updated_at, updated_by, is_deleted)
VALUES (3, 1.2, NOW(), "system", NOW(), "system", 0);
INSERT INTO rental_periods (duration_in_months, multiplier, created_at, created_by, updated_at, updated_by, is_deleted)
VALUES (6, 1.1, NOW(), "system", NOW(), "system", 0);
INSERT INTO rental_periods (duration_in_months, multiplier, created_at, created_by, updated_at, updated_by, is_deleted)
VALUES (12, 1.05, NOW(), "system", NOW(), "system", 0);

-- product_pricing - Singapore
INSERT INTO product_pricing (final_price, product_id, rental_period_id, region_id, created_at, created_by, updated_at, updated_by, is_deleted)
VALUES (1820000.0, 1, 1, 1, NOW(), "system", NOW(), "system", 0);
INSERT INTO product_pricing (final_price, product_id, rental_period_id, region_id, created_at, created_by, updated_at, updated_by, is_deleted)
VALUES (3320000.0, 1, 2, 1, NOW(), "system", NOW(), "system", 0);
INSERT INTO product_pricing (final_price, product_id, rental_period_id, region_id, created_at, created_by, updated_at, updated_by, is_deleted)
VALUES (6320000.0, 1, 3, 1, NOW(), "system", NOW(), "system", 0);

-- product_pricing - Malaysia
INSERT INTO product_pricing (final_price, product_id, rental_period_id, region_id, created_at, created_by, updated_at, updated_by, is_deleted)
VALUES (1825000.0, 1, 1, 2, NOW(), "system", NOW(), "system", 0);
INSERT INTO product_pricing (final_price, product_id, rental_period_id, region_id, created_at, created_by, updated_at, updated_by, is_deleted)
VALUES (3325000.0, 1, 2, 2, NOW(), "system", NOW(), "system", 0);
INSERT INTO product_pricing (final_price, product_id, rental_period_id, region_id, created_at, created_by, updated_at, updated_by, is_deleted)
VALUES (6325000.0, 1, 3, 2, NOW(), "system", NOW(), "system", 0);
