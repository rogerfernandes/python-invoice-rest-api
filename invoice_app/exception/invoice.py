class DefaultException(Exception):
    def __init__(self):
        self._message = None
        self._http_error_code = None

    def http_error_message(self):
        return self._message, self._http_error_code


class InvoiceNotFoundException(DefaultException):
    def __init__(self):
        self._message = None
        self._http_error_code = 204
