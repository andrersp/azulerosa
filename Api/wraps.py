# -*- coding: utf-8 -*-
""" 
    Wraps for check params for post endpoints and check role permission for access 
"""
from functools import wraps
from flask import request
from cerberus import Validator
from flask_jwt_extended import get_jwt_claims


class CustonValidator(Validator):

    def _validate_type_numeric(self, number):

        if not number:
            return True

        if isinstance(number, int):
            return True

        if isinstance(number, str):
            if number.isdigit():
                return True

        self._error()

    def _validate_description(self, description, field, value):
        """ Insert Description for swagger.
        The rule's arguments are validated against this schema:
        {'type': 'string'}
        """
        return


# Wraps validate data post
def required_params(schema):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):

            if not request.data:
                data = {}
            else:
                data = request.json

            v = CustonValidator(schema, lang="pt-BR")
            v.allow_unknown = False

            if not v.validate(data):
                return {"message": v.errors}, 400

            return fn(*args, **kwargs)
        return wrapper
    return decorator
