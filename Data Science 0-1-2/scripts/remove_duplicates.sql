DO $$
DECLARE
    deleted_rows INTEGER;
    initial_count INTEGER;
    final_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO initial_count FROM customers;
    RAISE NOTICE 'Initial row count: %', initial_count;
    
    SELECT COUNT(*) INTO deleted_rows
    FROM (
        SELECT *,
               LAG(event_time) OVER (
                   PARTITION BY event_type, product_id, user_id, price, user_session
                   ORDER BY event_time
               ) AS previous_time
        FROM customers
    ) sub
    WHERE previous_time IS NOT NULL
      AND event_time - previous_time <= INTERVAL '1 second';
    
    RAISE NOTICE 'Found % duplicate rows to be deleted', deleted_rows;

    DELETE FROM customers c
    USING (
        SELECT 
            ctid,
            LAG(event_time) OVER (
                PARTITION BY event_type, product_id, user_id, price, user_session
                ORDER BY event_time
            ) AS previous_time,
            event_time,
            event_type,
            product_id,
            user_id,
            price,
            user_session
        FROM customers
    ) dup
    WHERE c.ctid = dup.ctid
      AND dup.previous_time IS NOT NULL
      AND dup.event_time - dup.previous_time <= INTERVAL '1 second';

    SELECT COUNT(*) INTO final_count FROM customers;
    RAISE NOTICE 'Final row count: %', final_count;
    RAISE NOTICE 'Removed % duplicate rows', deleted_rows;
    
    RAISE NOTICE 'Duplicate removal completed successfully!';
END $$;
