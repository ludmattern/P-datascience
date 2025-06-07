
CREATE TABLE
	IF NOT EXISTS customers (
		event_time TIMESTAMP NOT NULL,
		event_type VARCHAR(50),
		product_id INTEGER,
		price DECIMAL(10, 2),
		user_id BIGINT,
		user_session UUID
	);

DO $$
DECLARE
    table_names TEXT[];
    table_name TEXT;
    sql_insert TEXT;
    row_count INTEGER;
BEGIN
    EXECUTE 'SELECT COUNT(*) FROM customers' INTO row_count;
    
    IF row_count > 0 THEN
        RAISE NOTICE 'Table customers already exists with data, insert ignored';
    ELSE
        SELECT ARRAY(
            SELECT tablename 
            FROM pg_tables 
            WHERE schemaname = 'public' 
            AND tablename LIKE 'data_202%'
            ORDER BY tablename
        ) INTO table_names;
        
        RAISE NOTICE 'Tables found: %', array_to_string(table_names, ', ');
        
        FOREACH table_name IN ARRAY table_names
        LOOP
            sql_insert := format('INSERT INTO customers (event_time, event_type, product_id, price, user_id, user_session) SELECT event_time, event_type, product_id, price, user_id, user_session FROM %I', table_name);
            
            EXECUTE sql_insert;
            RAISE NOTICE 'Data inserted from table: %', table_name;
            
            EXECUTE format('DROP TABLE IF EXISTS %I', table_name);
            RAISE NOTICE 'Table % dropped successfully', table_name;
        END LOOP;
        
        IF array_length(table_names, 1) > 0 THEN
            RAISE NOTICE 'Total of % tables processed and dropped', array_length(table_names, 1);
        ELSE
            RAISE NOTICE 'No data_202*_*** tables found';
        END IF;
    END IF;
END $$;