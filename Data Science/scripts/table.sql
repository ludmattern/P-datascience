CREATE TABLE
	IF NOT EXISTS data_2023_feb (
		event_time TIMESTAMP NOT NULL,
		event_type VARCHAR(50),
		product_id INTEGER,
		price DECIMAL(10, 2),
		user_id BIGINT,
		user_session UUID
	);

COPY data_2023_feb FROM	'/customer/data_2023_feb.csv' DELIMITER ',' CSV HEADER;
