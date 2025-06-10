DO $$
DECLARE
    csv_files TEXT[];
    file_name TEXT;
    sql_create TEXT;
    sql_copy TEXT;
    row_count INTEGER;
BEGIN
    SELECT ARRAY(
        SELECT regexp_replace(filename, '\.csv$', '')
        FROM pg_ls_dir('/customer') AS filename
        WHERE filename LIKE '%.csv'
        ORDER BY filename
    ) INTO csv_files;
    
    RAISE NOTICE 'Fichiers CSV trouvés: %', array_to_string(csv_files, ', ');
    
    FOREACH file_name IN ARRAY csv_files
    LOOP
        sql_create := format('
            CREATE TABLE IF NOT EXISTS %I (
                event_time TIMESTAMP NOT NULL,
                event_type VARCHAR(50),
                product_id INTEGER,
                price DECIMAL(10, 2),
                user_id BIGINT,
                user_session UUID
            );
        ', file_name);
        
        EXECUTE sql_create;
        
        EXECUTE format('SELECT COUNT(*) FROM %I', file_name) INTO row_count;
        
        IF row_count = 0 THEN
            sql_copy := format('
                COPY %I FROM %L DELIMITER %L CSV HEADER;
            ', file_name, '/customer/' || file_name || '.csv', ',');
            
            EXECUTE sql_copy;
            
            RAISE NOTICE 'Table % créée et données importées depuis %', file_name, file_name || '.csv';
        ELSE
            RAISE NOTICE 'Table % existe déjà avec des données, import ignoré', file_name;
        END IF;
    END LOOP;
END $$;
