from invoice_app.exception.invoice import InvoiceNotFoundException
from invoice_app.models.page import Page
from invoice_app.repository.invoice import InvoiceRepository
from invoice_app.models.invoice import Invoice
import math


class InvoiceService:
    def __init__(self, invoice_rep: InvoiceRepository):
        self.__invoice_rep = invoice_rep

    def get_invoice(self, document):
        result = self.__invoice_rep.get_invoice(document)
        if not result:
            raise InvoiceNotFoundException

        invoice = Invoice(**result[0])
        return invoice.to_json()

    def save_invoice(self, data):
        invoice = Invoice(**data)
        self.__invoice_rep.save_invoice(invoice)
        return invoice.to_json()

    def delete_invoice(self, document):
        if not self.__invoice_rep.get_invoice(document):
            raise InvoiceNotFoundException

        self.__invoice_rep.delete_invoice(document)

    def get_invoices(self, request_params):
        self._validate(request_params)

        result = self.__invoice_rep.get_invoices(request_params)
        count = self.__invoice_rep.count_invoices(request_params)
        response = self._build_response_page(count, result, request_params)

        return response.to_json()

    def _build_response_page(self, count, result, request_params):
        total_items = self._get_total_items(count)
        page_number = self._get_page_number(request_params)
        page_size = self._get_page_size(request_params)
        last_page = self._is_last_page(total_items, page_size, page_number)
        invoice_list = self._build_invoice_list(result)
        return Page(total_items, page_size, page_number, last_page, invoice_list)

    def _get_total_items(self, count):
        return count.get('count') if count else 0

    def _get_page_number(self, request_params):
        return request_params.get('page_number') if request_params.get('page_number') else 1

    def _get_page_size(self, request_params):
        return request_params.get('page_size') if request_params.get('page_size') else 20

    def _is_last_page(self, total_items, page_size, page_number):
        return math.ceil(int(total_items) / int(page_size)) == int(page_number)

    def _build_invoice_list(self, result):
        invoice_list = []
        for invoice in result:
            invoice_list.append(Invoice(**invoice).to_json())
        return invoice_list

    def _validate(self, request_params: dict):
        print(request_params)
        for value in request_params.values():
            pass
