# python-invoice-rest-api
Invoice Python API

pipenv

```
GET
http://localhost/api/v1/invoices?reference_year=2020&reference_month=2&document=123&sort=reference_year&dir=desc&page_size=10&page_number=2

POST
http://localhost/api/v1/invoice
{
    'document': '12345',
    'description': 'Nota Fiscal 12345',
    'amount': 800.23,
    'reference_month': 8,
    'reference_year': 2020
}

GET, DELETE
http://localhost/api/v1/invoice/12345

```

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

CREATE USER app@'%' IDENTIFIED BY 'pass';

GRANT INSERT, DELETE, SELECT, UPDATE ON invoice_store.* TO 'app'@'%';

flush privileges;
```