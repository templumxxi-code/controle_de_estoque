ALTER TABLE users ADD COLUMN full_name VARCHAR(180) NULL;
ALTER TABLE users ADD COLUMN phone VARCHAR(40) NULL;
ALTER TABLE users ADD COLUMN job_title VARCHAR(120) NULL;
ALTER TABLE users ADD COLUMN role VARCHAR(30) NOT NULL DEFAULT 'operator';
ALTER TABLE users ADD COLUMN must_change_password BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE users ADD COLUMN last_login_at DATETIME NULL;
ALTER TABLE users ADD COLUMN theme_preference VARCHAR(10) NOT NULL DEFAULT 'dark';
ALTER TABLE users ADD COLUMN updated_at DATETIME NULL;

CREATE TABLE audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    action VARCHAR(60) NOT NULL,
    entity VARCHAR(60) NULL,
    entity_id INT NULL,
    description VARCHAR(500) NOT NULL,
    result VARCHAR(20) NOT NULL DEFAULT 'success',
    ip_address VARCHAR(45) NULL,
    metadata_json TEXT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX ix_audit_user_id (user_id),
    INDEX ix_audit_action (action),
    INDEX ix_audit_created_at (created_at),
    CONSTRAINT fk_audit_user FOREIGN KEY (user_id) REFERENCES users(id)
);