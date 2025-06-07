DO $$
DECLARE
    customers_count  INTEGER;
    items_count      INTEGER;
    updated_rows     INTEGER;
BEGIN
    SELECT COUNT(*) INTO customers_count FROM customers;
    SELECT COUNT(*) INTO items_count     FROM item;

    RAISE NOTICE 'Initial customers count : %', customers_count;
    RAISE NOTICE 'Initial items count     : %', items_count;

    ALTER TABLE customers
        ADD COLUMN IF NOT EXISTS category_id   BIGINT,
        ADD COLUMN IF NOT EXISTS category_code VARCHAR(100),
        ADD COLUMN IF NOT EXISTS brand         VARCHAR(100);

    RAISE NOTICE 'Added missing columns to customers table (if any)';

    CREATE INDEX IF NOT EXISTS idx_item_product_id      ON item(product_id);
    CREATE INDEX IF NOT EXISTS idx_customers_product_id ON customers(product_id);

    WITH src AS (
        SELECT product_id,
               category_id,
               category_code,
               brand
        FROM item
    )
    UPDATE customers AS c
       SET category_id   = s.category_id,
           category_code = s.category_code,
           brand         = s.brand
      FROM src AS s
     WHERE s.product_id = c.product_id
       AND (c.category_id   IS DISTINCT FROM s.category_id
        OR  c.category_code IS DISTINCT FROM s.category_code
        OR  c.brand         IS DISTINCT FROM s.brand);

    GET DIAGNOSTICS updated_rows = ROW_COUNT;
    RAISE NOTICE 'Updated % customer rows with item information', updated_rows;

    SELECT COUNT(*) INTO customers_count FROM customers;
    RAISE NOTICE 'Final customers count : %', customers_count;

    RAISE NOTICE 'Fusion completed successfully! Customers table now includes item information.';
END $$;
