-- Proposed staging schema for DanangTrip crawler.
-- These tables should be reviewed before applying to the real database.

CREATE TABLE crawl_sources (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100) NOT NULL,
    config_json JSONB,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    last_run_at TIMESTAMP NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE crawl_jobs (
    id BIGSERIAL PRIMARY KEY,
    source_id BIGINT NOT NULL REFERENCES crawl_sources(id),
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    started_at TIMESTAMP NULL,
    finished_at TIMESTAMP NULL,
    error_message TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE crawl_items (
    id BIGSERIAL PRIMARY KEY,
    source_id BIGINT NULL REFERENCES crawl_sources(id),
    job_id BIGINT NULL REFERENCES crawl_jobs(id),
    entity_type VARCHAR(100) NOT NULL,
    external_id VARCHAR(255) NULL,
    source_url TEXT NULL,
    raw_payload JSONB NOT NULL,
    normalized_payload JSONB NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'raw',
    duplicate_of_id BIGINT NULL REFERENCES crawl_items(id),
    reviewed_by BIGINT NULL,
    reviewed_at TIMESTAMP NULL,
    published_entity_type VARCHAR(100) NULL,
    published_entity_id BIGINT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_crawl_items_entity_status ON crawl_items(entity_type, status);
CREATE INDEX idx_crawl_items_external_id ON crawl_items(external_id);

CREATE TABLE crawl_logs (
    id BIGSERIAL PRIMARY KEY,
    job_id BIGINT NULL REFERENCES crawl_jobs(id),
    level VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    context_json JSONB NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

