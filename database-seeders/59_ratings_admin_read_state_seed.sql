BEGIN;

-- Initialize historical admin read state only once.
-- Later incremental runs must preserve ratings marked as viewed by an admin.
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM settings
        WHERE key = 'data.ratings_admin_read_state_initialized_v1'
    ) THEN
        UPDATE ratings
        SET is_new = created_at >= CURRENT_TIMESTAMP - INTERVAL '7 days';

        INSERT INTO settings (
            key,
            value,
            value_type,
            is_public,
            created_at,
            updated_at
        )
        VALUES (
            'data.ratings_admin_read_state_initialized_v1',
            CURRENT_TIMESTAMP::text,
            'string',
            false,
            CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP
        );
    END IF;
END
$$;

COMMIT;
