from unittest import TestCase
from unittest.mock import Mock, ANY

from invoice_app.exceptions.invoice import InvoiceNotFoundException, InvalidQueryParameterException
from invoice_app.models.invoice import Invoice
from invoice_app.repositories.invoice import InvoiceRepository
from invoice_app.services.invoice import InvoiceService


class TestInvoiceModel(TestCase):
    def test_to_json_should_return_model_json(self):
        document = '123'
        description = 'Descrição'
        amount = 123.12
        reference_month = 4
        reference_year = 2020
        invoice = Invoice(document, description, amount, reference_month, reference_year)

        actual = invoice.to_json()
        self.assertEqual(document, actual.get('document'))
        self.assertEqual(description, actual.get('description'))
        self.assertEqual(amount, actual.get('amount'))
        self.assertEqual(reference_month, actual.get('reference_month'))
        self.assertEqual(reference_year, actual.get('reference_year'))
        self.assertIsNotNone(actual.get('created_at'))

    def test_is_active_should_return_true(self):
        invoice = Invoice('123', 'Descrição', 123.12, 4, 2020)

        actual = invoice.is_active()

        self.assertTrue(actual)

    def test_insert_values_should_return_insert_values(self):
        expected = ('123', 'Descrição', '123.12', 4, 2020, True, ANY)
        invoice = Invoice('123', 'Descrição', 123.12, 4, 2020)

        actual = invoice.insert_values()

        self.assertEqual(expected, actual)

    def test_insert_projection_should_return_insert_projection_string(self):
        expected = 'document, description, amount, reference_month, reference_year, is_active, created_at'
        invoice = Invoice('123', 'Descrição', 123.12, 4, 2020)

        actual = invoice.insert_projection()

        self.assertEqual(expected, actual)


class TestInvoiceService(TestCase):
    def test_get_invoice_should_return_expected_data_when_invoice_found(self):
        expected = {'amount': 1233.23,
                    'created_at': '2020-04-01',
                    'description': 'Primeira nota',
                    'document': '123',
                    'reference_month': 2,
                    'reference_year': 2020}
        repository = Mock()
        repository.get_invoice.return_value = [{'document': '123',
                                                'description': 'Primeira nota',
                                                'amount': 1233.23,
                                                'reference_month': 2,
                                                'reference_year': 2020,
                                                'is_active': 1,
                                                'created_at': '2020-04-01',
                                                'deactive_at': None}]
        invoice_service = InvoiceService(repository)

        actual = invoice_service.get_invoice('123')

        self.assertEqual(expected, actual)

    def test_get_invoice_should_raise_exception_when_invoice_not_found(self):
        repository = Mock()
        repository.get_invoice.return_value = []
        invoice_service = InvoiceService(repository)

        self.assertRaises(InvoiceNotFoundException, lambda: invoice_service.get_invoice('123'))

    def test_save_invoice_should_save_invoice(self):
        expected = {'amount': 300.0,
                    'created_at': '2020-04-01',
                    'description': 'Descrição da nota fiscal',
                    'document': '123456',
                    'reference_month': 3,
                    'reference_year': 2020}
        data = {
            'document': '123456',
            'description': 'Descrição da nota fiscal',
            'amount': 300.00,
            'reference_year': 2020,
            'reference_month': 3,
            'created_at': '2020-04-01',
            'deactive_at': None
        }
        repository = Mock()
        invoice_service = InvoiceService(repository)

        actual = invoice_service.save_invoice(data)

        repository.save_invoice.assert_called_once()
        self.assertEqual(expected, actual)

    def test_delete_invoice_should_delete_invoice(self):
        repository = Mock()
        repository.get_invoice.return_value = ANY
        invoice_service = InvoiceService(repository)

        invoice_service.delete_invoice('123')

        repository.get_invoice.assert_called_once()
        repository.delete_invoice.assert_called_once()

    def test_delete_invoice_should_raise_exception(self):
        repository = Mock()
        repository.get_invoice.return_value = []
        invoice_service = InvoiceService(repository)

        self.assertRaises(InvoiceNotFoundException, lambda: invoice_service.delete_invoice('123'))
        repository.get_invoice.assert_called_once()

    def test_get_invoices_should_return_invoices(self):
        expected = {'page_size': '10',
                    'page_number': '1',
                    'total_items': 1,
                    'last_page': True,
                    'data': [{'amount': 1233.23,
                              'created_at': '2020-04-01',
                              'description': 'Primeira nota',
                              'document': '123',
                              'reference_month': 2,
                              'reference_year': 2020}]
                    }
        params = {'reference_year': '2020',
                  'reference_month': '2',
                  'document': '123',
                  'sort': 'reference_year',
                  'dir': 'desc',
                  'page_size': '10',
                  'page_number': '1'}

        repository = Mock()
        repository.get_invoices.return_value = [{'document': '123',
                                                 'description': 'Primeira nota',
                                                 'amount': 1233.23,
                                                 'reference_month': 2,
                                                 'reference_year': 2020,
                                                 'is_active': 1,
                                                 'created_at': '2020-04-01',
                                                 'deactive_at': None}]
        repository.count_invoices.return_value = {'count': 1}
        invoice_service = InvoiceService(repository)

        actual = invoice_service.get_invoices(params)

        self.assertEqual(expected, actual)

    def test_get_invoices_should_raise_exception_when_params_has_db_reserved_characters(self):
        params = {'reference_year': '2020) and is true, ('}
        repository = Mock()
        invoice_service = InvoiceService(repository)

        self.assertRaises(InvalidQueryParameterException, lambda: invoice_service.get_invoices(params))


class TestInvoiceRepository(TestCase):
    def test_get_invoice_should_return_invoice(self):
        query = 'select document, description, amount, reference_month, reference_year, is_active, created_at,' \
                'deactive_at from invoice where document = %s and is_active is true'
        param = ('123',)
        expected = [{'any': 'any'}]
        database = Mock()
        connection = Mock()
        cursor = Mock()
        database.get_connection.return_value = connection
        connection.cursor.return_value = cursor
        cursor.fetchall.return_value = [{'any': 'any'}]
        invoice_repository = InvoiceRepository(database)

        actual = invoice_repository.get_invoice('123')

        cursor.execute.assert_called_once_with(query, param)
        cursor.fetchall.assert_called_once()
        self.assertEqual(expected, actual)

    def test_save_invoice_should_save_invoice(self):
        query = "insert into invoice ( document, description, amount, reference_month, reference_year, is_active, " \
                "created_at ) values ('123', 'Descrição', '123.12', 4, 2020, True, '2020-04-01')"
        database = Mock()
        connection = Mock()
        cursor = Mock()
        database.get_connection.return_value = connection
        connection.cursor.return_value = cursor
        cursor.execute.return_value = None
        invoice_repository = InvoiceRepository(database)
        invoice = Invoice('123', 'Descrição', 123.12, 4, 2020, True, '2020-04-01')

        invoice_repository.save_invoice(invoice)

        cursor.execute.assert_called_once_with(query)
        cursor.fetchall.assert_not_called()

    def test_delete_invoice_should_delete_invoice(self):
        query = 'update invoice set is_active = false, deactive_at = %s where document = %s'
        param = (ANY, '123')
        database = Mock()
        connection = Mock()
        cursor = Mock()
        database.get_connection.return_value = connection
        connection.cursor.return_value = cursor
        cursor.execute.return_value = None
        invoice_repository = InvoiceRepository(database)

        invoice_repository.delete_invoice('123')

        cursor.execute.assert_called_once_with(query, param)
        cursor.fetchall.assert_not_called()

    def test_count_invoice_should_return_count_found_invoices(self):
        expected = {'count': 1}
        database = Mock()
        connection = Mock()
        cursor = Mock()
        database.get_connection.return_value = connection
        connection.cursor.return_value = cursor
        cursor.execute.return_value = None
        cursor.fetchall.return_value = [{'count': 1}]
        invoice_repository = InvoiceRepository(database)
        params = {'param': 'value'}

        actual = invoice_repository.count_invoices(params)

        cursor.execute.assert_called_once()
        cursor.fetchall.assert_called_once()
        self.assertEqual(expected, actual)

    def test_get_invoices_should_return_invoices_without_parameters(self):
        query = 'select document, description, amount, reference_month, reference_year, is_active, created_at, ' \
                'deactive_at from invoice where is_active is true order by id limit 20 offset 0'
        database = Mock()
        connection = Mock()
        cursor = Mock()
        database.get_connection.return_value = connection
        connection.cursor.return_value = cursor
        invoice_repository = InvoiceRepository(database)
        params = {}

        invoice_repository.get_invoices(params)

        cursor.execute.assert_called_once_with(query)
        cursor.fetchall.assert_called_once()

    def test_get_invoices_should_return_invoices_with_filter_parameter(self):
        query = 'select document, description, amount, reference_month, reference_year, is_active, created_at, ' \
                'deactive_at from invoice where is_active is true and reference_year = 2020 order by id limit 20 ' \
                'offset 0'
        database = Mock()
        connection = Mock()
        cursor = Mock()
        database.get_connection.return_value = connection
        connection.cursor.return_value = cursor
        invoice_repository = InvoiceRepository(database)
        params = {'reference_year': 2020}

        invoice_repository.get_invoices(params)

        cursor.execute.assert_called_once_with(query)
        cursor.fetchall.assert_called_once()

    def test_get_invoices_should_return_invoices_with_sort_parameter(self):
        query = 'select document, description, amount, reference_month, reference_year, is_active, created_at, ' \
                'deactive_at from invoice where is_active is true order by document limit 20 offset 0'
        database = Mock()
        connection = Mock()
        cursor = Mock()
        database.get_connection.return_value = connection
        connection.cursor.return_value = cursor
        invoice_repository = InvoiceRepository(database)
        params = {'sort': 'document'}

        invoice_repository.get_invoices(params)

        cursor.execute.assert_called_once_with(query)
        cursor.fetchall.assert_called_once()

    def test_get_invoices_should_return_invoices_with_page_parameter(self):
        query = 'select document, description, amount, reference_month, reference_year, is_active, created_at, ' \
                'deactive_at from invoice where is_active is true order by id limit 7 offset 7'
        database = Mock()
        connection = Mock()
        cursor = Mock()
        database.get_connection.return_value = connection
        connection.cursor.return_value = cursor
        invoice_repository = InvoiceRepository(database)
        params = {'page_size': 7, 'page_number': 2}

        invoice_repository.get_invoices(params)

        cursor.execute.assert_called_once_with(query)
        cursor.fetchall.assert_called_once()
