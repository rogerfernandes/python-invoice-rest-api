# python-invoice-rest-api
Invoice Python API

pipenv

```sql
CREATE DATABASE invoice_store;

CREATE TABLE IF NOT EXISTS invoice_store.invoice (
    id INT NOT NULL AUTO_INCREMENT,
    document VARCHAR(14),
    description VARCHAR(256),
    amount DECIMAL(16, 2),
    reference_month INTEGER,
    reference_year INTEGER,
    is_active BOOLEAN,
    created_at DATETIME,
    deactive_at DATETIME,
    PRIMARY KEY (id)
);
```