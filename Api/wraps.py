# -*- coding: utf-8 -*-
"""
    Wraps for check params for post endpoints and check role permission for access
"""
from functools import wraps
from flask import request
from cerberus import Validator
from flask_jwt_extended import get_jwt_claims

from inc import validate_registation


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

    def _check_with_registration(self, field, value):

        type_reg = self.document.get("type_registration")

        if not value:
            self._error(field, "empty values not allowed")
            return     
               

        if type_reg == 1:

            if not validate_registation.validar_cpf(value):
                self._error(field, "Valid cpf required")
                return            

        if type_reg == 2:

            if not validate_registation.validar_cnpj(value):
                self._error(field, "Valid cnpj required")

            # try:
            #     cnpj = validate_cnpj.CNPJ(value)

            #     if not cnpj.valido():
            #         self._error(field, "Valid cnpj required")
            #         return
            # except Exception as err:
            #     self._error(field, str(err))
            #     return  


        
    
    def _check_with_cellcheck(self, field, value):

        phone = self.document.get("phone")


        if not phone and not value:
            self._error(field, "At least one contact number is required")
            return False
        
        if value and len(value) < 10:
            self._error(field, "min length is 10")
            return False
        
        if value and len(value) > 11:
            self._error(field, "max length is 11")
            return False
    
    def _check_with_phonecheck(self, field, value):

        cell_phone = self.document.get("cell_phone")


        if not cell_phone and not value:
            self._error(field, "At least one contact number is required")
            return False
        
        if value and len(value) < 10:
            self._error(field, "min length is 10")
            return False
        
        if value and len(value) > 11:
            self._error(field, "max length is 11")
            return False


        
        
        
                



        

        
        

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
