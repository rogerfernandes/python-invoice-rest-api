from unittest import TestCase

from invoice_app.models.page import Page


class TestPage(TestCase):
    def test_to_json_should_return_json(self):
        expected = {
            'total_items': 100,
            'page_size': 10,
            'page_number': 1,
            'last_page': False,
            'data': [{'any': 'any'}]}
        page = Page(100, 10, 1, False, [{'any': 'any'}])

        actual = page.to_json()

        self.assertEqual(expected, actual)
