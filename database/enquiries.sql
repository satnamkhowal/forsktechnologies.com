-- Optional storage for the reusable Forsk Technologies enquiry system.
-- Configure FORSK_ENQUIRY_DB_DSN / USER / PASS only on the server.

CREATE TABLE IF NOT EXISTS forsk_enquiries (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    request_id VARCHAR(32) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(254) NOT NULL,
    phone VARCHAR(25) NOT NULL,
    company VARCHAR(120) NULL,
    message TEXT NOT NULL,
    source_page VARCHAR(255) NULL,
    source_form VARCHAR(80) NULL,
    created_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_forsk_enquiries_request_id (request_id),
    KEY idx_forsk_enquiries_created_at (created_at),
    KEY idx_forsk_enquiries_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
