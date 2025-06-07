CREATE TABLE
	IF NOT EXISTS item (
		product_id INTEGER,
		category_id BIGINT,
		category_code VARCHAR(255),
		brand VARCHAR(100)
	);

COPY item FROM '/item/item.csv' DELIMITER ',' CSV HEADER;
