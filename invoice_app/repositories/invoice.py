import datetime
from datetime import datetime

from invoice_app.extensions.database import Database
from invoice_app.models.invoice import Invoice


class InvoiceRepository:
    def __init__(self, db_instance: Database):
        self._database = db_instance

    def get_invoice(self, document):
        query = 'select document, description, amount, reference_month, reference_year, is_active, created_at,' \
                'deactive_at from invoice where document = %s and is_active is true'
        return self._execute_query(query, (document,))

    def save_invoice(self, invoice: Invoice):
        query = f'insert into invoice ( {invoice.insert_projection()} ) values {invoice.insert_values()}'
        return self._execute_query(query)

    def delete_invoice(self, document):
        query = 'update invoice set is_active = false, deactive_at = %s where document = %s'
        self._execute_query(query, (datetime.now(), document))

    def count_invoices(self, query_params):
        query = self._build_count_invoices_query(query_params)
        return self._execute_query(query)[0]

    def get_invoices(self, query_params):
        query = self._build_get_invoices_query(query_params)
        return self._execute_query(query)

    def _build_count_invoices_query(self, query_params: dict):
        query = 'select count(id) as count from invoice where is_active is true'
        query = self._build_get_invoices_query_filter(query, query_params)
        return query

    def _build_get_invoices_query(self, query_params: dict):
        query = 'select document, description, amount, reference_month, reference_year, is_active, created_at, ' \
                'deactive_at from invoice where is_active is true'
        query = self._build_get_invoices_query_filter(query, query_params)
        query = self._build_get_invoices_query_sort(query, query_params.get('sort'), query_params.get('dir'))
        query = self._build_get_invoices_query_page(query, query_params.get('page_size'),
                                                    query_params.get('page_number'))
        return query

    def _build_get_invoices_query_filter(self, query: str, query_params: dict):
        if query_params.get('reference_year'):
            query = query + f' and reference_year = {query_params.get("reference_year")}'
        if query_params.get('reference_month'):
            query = query + f' and reference_month = {query_params.get("reference_month")}'
        if query_params.get('document'):
            query = query + f' and document = \'{str(query_params.get("document"))}\''
        return query

    def _build_get_invoices_query_sort(self, query: str, sort_param: str, dir_param: str):
        if sort_param:
            query = query + ' order by'
            for param in sort_param.split(','):
                query = query + f' {param} {dir_param},' if dir_param else query + f' {param},'
            if query.endswith(','):
                query = query[0:len(query) - 1]
        else:
            query = query + ' order by id'
        return query

    def _build_get_invoices_query_page(self, query: str, page_size_param: int, page_number_param: int):
        page_size = int(page_size_param) if page_size_param else 20
        page_number = int(page_number_param) - 1 if page_number_param else 0
        offset = page_number * page_size
        query = query + f' limit {page_size} offset {offset}'
        return query

    def _execute_query(self, query: str, params=None):
        conn = self._database.get_connection()
        cur = conn.cursor(dictionary=True)

        result = cur.execute(query) if params is None else cur.execute(query, params)

        if query.lower().startswith('select'):
            result = cur.fetchall()

        conn.commit()
        cur.close()

        return result
