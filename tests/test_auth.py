from unittest import TestCase
from unittest.mock import patch

from invoice_app.services.auth import requires_authentication


class TestAuthService(TestCase):

    @patch('invoice_app.services.auth.request')
    def test_requires_authentication_should_authenticate_request(self, mock_request):
        expected = 'Invoice'
        mock_request.headers = {'X-Api-Key': 'NDAwZGEyNDEtMjMxMS00YWY0LTg5NjktZTAwZWEwOTUyYmQ4Cg=='}

        @requires_authentication
        def decorated_func(invoice='Invoice'):
            return invoice

        actual = decorated_func()

        self.assertEqual(expected, actual)

    @patch('invoice_app.services.auth.request')
    def test_requires_authentication_should_deny_request_when_api_key_is_wrong(self, mock_request):
        expected = ({'message': 'Header X-Api-Key type string, is missing or invalid'}, 401)
        mock_request.headers = {'X-Api-Key': ''}

        @requires_authentication
        def decorated_func(invoice='Invoice'):
            return invoice

        actual = decorated_func()

        self.assertEqual(expected, actual)

    @patch('invoice_app.services.auth.request')
    def test_requires_authentication_should_deny_request_when_api_key_is_not_exists(self, mock_request):
        expected = ({'message': 'Header X-Api-Key type string, is missing or invalid'}, 401)
        mock_request.headers = {}

        @requires_authentication
        def decorated_func(invoice='Invoice'):
            return invoice

        actual = decorated_func()

        self.assertEqual(expected, actual)
