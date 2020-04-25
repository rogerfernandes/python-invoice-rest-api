from flask import Flask, request
from flask_restful import Resource, Api, reqparse, marshal_with, fields

from invoice_app.exceptions.invoice import InvoiceNotFoundException, InvalidQueryParameterException
from invoice_app.extensions import database, configuration
from invoice_app.repositories.invoice import InvoiceRepository
from invoice_app.services.auth import requires_authentication
from invoice_app.services.invoice import InvoiceService

app = Flask(__name__)
configuration.init_app(app)
database.init_db(app)
api_v1 = Api(app, '/api/v1')

db = database.Database(app.config)
rep = InvoiceRepository(db)
invoice_service = InvoiceService(rep)


class InvoiceResource(Resource):
    params = reqparse.RequestParser()
    params.add_argument('document', type=str, required=True, help='Missing required parameter')
    params.add_argument('description', type=str, required=True, help='Missing required parameter')
    params.add_argument('amount', type=float, required=True, help='Missing required parameter')
    params.add_argument('reference_month', type=int, required=True, help='Missing required parameter')
    params.add_argument('reference_year', type=int, required=True, help='Missing required parameter')

    m_fields = {
        'document': fields.String,
        'description': fields.String,
        'amount': fields.Float,
        'reference_month': fields.Integer,
        'reference_year': fields.Integer,
        'created_at': fields.String
    }

    @requires_authentication
    @marshal_with(m_fields, 'data')
    def get(self, document):
        try:
            return invoice_service.get_invoice(document)

        except InvoiceNotFoundException as invoice_not_found_exception:
            ex = invoice_not_found_exception.http_error_message()

        except Exception as err:
            print('Internal Error: ', err)
            ex = {'message': 'An error occurred while trying to fetch an Invoice'}, 500

        return ex

    @requires_authentication
    @marshal_with(m_fields, 'data')
    def post(self):
        content_type = request.content_type
        if not content_type or content_type != 'application/json':
            return 'Unsupported Media Type, required application/json', 415

        data = InvoiceResource.params.parse_args()
        try:
            return invoice_service.save_invoice(data), 201
        except Exception as err:
            print('Internal Error: ', err)
            return {'message': 'An error occurred while trying to save an Invoice'}, 500

    @requires_authentication
    def delete(self, document):
        try:
            invoice_service.delete_invoice(document)
            return None, 204

        except InvoiceNotFoundException as invoice_not_found_exception:
            ex = invoice_not_found_exception.http_error_message()

        except Exception as err:
            print('Internal Error: ', err)
            ex = {'message': 'An error occurred while trying to fetch an Invoice'}, 500

        return ex


class InvoicesResource(Resource):
    m_fields = {
        'document': fields.String,
        'description': fields.String,
        'amount': fields.Float,
        'reference_month': fields.Integer,
        'reference_year': fields.Integer,
        'created_at': fields.String
    }

    m_page_fields = {
        'page_size': fields.Integer,
        'page_number': fields.Integer,
        'total_items': fields.Integer,
        'last_page': fields.Boolean,
        'data': fields.Nested(m_fields)
    }

    @requires_authentication
    @marshal_with(m_page_fields)
    def get(self):
        try:
            return invoice_service.get_invoices(request.args)

        except InvalidQueryParameterException as e:
            return e.http_error_message()

        except Exception as e:
            print(e)
            return {'message': 'An error occurred while trying to fetch Invoices'}, 500


api_v1.add_resource(InvoiceResource, '/invoice', '/invoice/<document>')
api_v1.add_resource(InvoicesResource, '/invoices')

if __name__ == '__main__':
    app.run('0.0.0.0', 3000)
