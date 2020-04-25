from functools import wraps

from flask import request

from config import API_KEYS

_authentication_header = 'X-Api-Key'


def requires_authentication(fn):
    @wraps(fn)
    def authenticate(*args, **kwargs):
        if _is_present_authentication_header() and _is_present_token_in_api_keys():
            return fn(*args, **kwargs)
        else:
            return {"message": f'Header {_authentication_header} type string, is missing or invalid'}, 401

    return authenticate


def _is_present_authentication_header():
    return _authentication_header in request.headers


def _is_present_token_in_api_keys():
    return request.headers[_authentication_header] in API_KEYS
