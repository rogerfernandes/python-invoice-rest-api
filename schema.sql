CREATE DATABASE IF NOT EXISTS invoice_store;

CREATE TABLE IF NOT EXISTS invoice_store.invoice
(
    id              INT NOT NULL AUTO_INCREMENT,
    document        VARCHAR(14),
    description     VARCHAR(256),
    amount          DECIMAL(16, 2),
    reference_month INTEGER,
    reference_year  INTEGER,
    is_active       BOOLEAN,
    created_at      DATETIME,
    deactive_at     DATETIME,
    PRIMARY KEY (id)
);

CREATE USER IF NOT EXISTS app@'%' IDENTIFIED BY 'pass';

GRANT INSERT, DELETE, SELECT, UPDATE ON invoice_store.* TO 'app'@'%';

flush privileges;