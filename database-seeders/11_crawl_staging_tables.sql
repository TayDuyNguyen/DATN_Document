-- DanangTrip Crawler Staging Tables
-- FILE: 11_crawl_staging_tables.sql
-- Purpose:
--   Store crawled data before admin review.
--   Do not publish records directly into production tables.

CREATE TABLE IF NOT EXISTS crawl_sources (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100) NOT NULL,
    config_json JSONB,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    last_run_at TIMESTAMP NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX IF NOT EXISTS crawl_sources_name_unique
    ON crawl_sources (name);

CREATE TABLE IF NOT EXISTS crawl_jobs (
    id BIGSERIAL PRIMARY KEY,
    source_id BIGINT NOT NULL REFERENCES crawl_sources(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    started_at TIMESTAMP NULL,
    finished_at TIMESTAMP NULL,
    error_message TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS crawl_items (
    id BIGSERIAL PRIMARY KEY,
    source_id BIGINT NULL REFERENCES crawl_sources(id) ON DELETE SET NULL,
    job_id BIGINT NULL REFERENCES crawl_jobs(id) ON DELETE SET NULL,
    entity_type VARCHAR(100) NOT NULL,
    external_id VARCHAR(255) NULL,
    source_url TEXT NULL,
    raw_payload JSONB NOT NULL,
    normalized_payload JSONB NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'raw',
    duplicate_of_id BIGINT NULL REFERENCES crawl_items(id) ON DELETE SET NULL,
    reviewed_by BIGINT NULL REFERENCES users(id) ON DELETE SET NULL,
    reviewed_at TIMESTAMP NULL,
    published_entity_type VARCHAR(100) NULL,
    published_entity_id BIGINT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX IF NOT EXISTS crawl_items_source_external_unique
    ON crawl_items (source_id, external_id)
    WHERE external_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_crawl_items_entity_status
    ON crawl_items (entity_type, status);

CREATE INDEX IF NOT EXISTS idx_crawl_items_external_id
    ON crawl_items (external_id);

CREATE INDEX IF NOT EXISTS idx_crawl_items_normalized_payload_gin
    ON crawl_items USING GIN (normalized_payload);

CREATE TABLE IF NOT EXISTS crawl_logs (
    id BIGSERIAL PRIMARY KEY,
    job_id BIGINT NULL REFERENCES crawl_jobs(id) ON DELETE SET NULL,
    level VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    context_json JSONB NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

