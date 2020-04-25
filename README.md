# python-invoice-rest-api
- Rest API to store Invoices

## Running on Docker
- Docker-compose will run the application and a MySql database
- Application `http://localhost:80`
- Database `http://localhost:3306`

### Prerequisites
- Docker
- docker-compose

### Commands
- RUN: `docker-compose up -d` (this command is used to create and start containers)
- STOP: `docker-compose stop`
- START `docker-compose start`

## Running Locally
- Application `http://localhost:80`
- Database must be configured

### Prerequisites
- python3.7
- pip3
- pipenv

### Commands
- RUN: `pipenv run python app.py`
- STOP: `Ctrl + C`
- RUN TESTS: `python3 -m unittest`

# Using
 - Just to remember that locally port is `:3000` and in the Docker container is `:80`
## Invoice end-points

### GET
- Request
    - Path Param `document`
    - Header `X-Api-Key` (application token)
```
curl -i -X GET 'localhost:3000/api/v1/invoice/123456' \
--header 'X-Api-Key: NDAwZGEyNDEtMjMxMS00YWY0LTg5NjktZTAwZWEwOTUyYmQ4Cg=='
```
- Response
    - Body `Invoice`
    - Http Status Code `200 OK`
```
{
    "data": {
        "document": "123456",
        "description": "Invoice 123456",
        "amount": 123.23,
        "reference_month": 4,
        "reference_year": 2020,
        "created_at": "2020-04-25 00:00:00"
    }
}
```

### POST
- Request
    - Header `Content-Type` must be `application/json`
    - Header `X-Api-Key` (application token)
    - Body `Invoice`
```
curl -i -X POST 'localhost:3000/api/v1/invoice' \
--header 'X-Api-Key: NDAwZGEyNDEtMjMxMS00YWY0LTg5NjktZTAwZWEwOTUyYmQ4Cg==' \
--header 'Content-Type: application/json' \
--data-raw '{
    "document": "123456",
    "description": "Invoice 123456",
    "amount": 123.23,
    "reference_year": 2020,
    "reference_month": 4
}'
```
 - Response
    - Body `Invoice`
    - Http Status Code `201 CREATED`
```
{
    "data": {
        "document": "123456",
        "description": "Invoice 123456",
        "amount": 123.23,
        "reference_month": 4,
        "reference_year": 2020,
        "created_at": "2020-04-25 00:00:00"
    }
}
```

### DELETE
- Request
    - Path Param `document`
    - Header `X-Api-Key` (application token)
```
curl -i -X DELETE 'localhost:3000/api/v1/invoice/123456' \
--header 'X-Api-Key: NDAwZGEyNDEtMjMxMS00YWY0LTg5NjktZTAwZWEwOTUyYmQ4Cg=='
```
- Response
    - Http Status Code `204 NO CONTENT`
    
## Invoices end-point

### GET
- Request
    - Query Params
        - document - Invoice document `string`
        - reference_month - Invoice month `int`
        - reference_year - Invoice year `int`
        - sort - by document, reference_month and reference_year `string`
        - dir - ASC(Default) and DESC `string`
        - page_size - Invoices per page `int`
        - page_number - Page number `int`
    - Header `X-Api-Key` (application token)
```
curl -i -X GET 'http://localhost/api/v1/invoices?reference_year=2020&reference_month=1&document=123456&sort=reference_year&dir=desc&page_size=10&page_number=1' \
--header 'X-Api-Key: NDAwZGEyNDEtMjMxMS00YWY0LTg5NjktZTAwZWEwOTUyYmQ4Cg=='
```
- Response
     - Paginated Invoices
```
{
    "page_size": 10,
    "page_number": 1,
    "total_items": 1,
    "last_page": true,
    "data": [
        {
            "document": "123456",
            "description": "Invoice 123456",
            "amount": 1233.23,
            "reference_month": 4,
            "reference_year": 2020,
            "created_at": "2020-04-22 00:00:00"
        }
    ]
}
```

# Configuration
## API Keys
- You can configure multiple API Keys in `config.py` file to authenticate requests to the application

## Environment Vars
- You can configure env vars in .env file
    - FLASK_ENV=development
    - FLASK_DEBUG=true
    - FLASK_DB_USER=app
    - FLASK_DB_PASSWORD=pass
    - FLASK_DB_HOST=localhost
    - FLASK_DB_DATABASE=invoice_store `this variable cannot be modified at the moment, because there is hard code in the application, because we are not using ORM` 
    - FLASK_DB_ROOT_PASSWORD=123456 `this password is used to run migration in database`

## Docker-compose
- You can change MySql `root` password
    - FLASK_DB_ROOT_PASSWORD: 123456
    - MYSQL_ROOT_PASSWORD: 123456