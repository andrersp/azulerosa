# -*- coding: utf-8 -*-
import re
from cerberus import Validator
from datetime import datetime
from inc.cpf_cnpj_validator import validate_cnpj, validate_cpf


class CustomValidator2(Validator):

    def to_date(s): return datetime.strptime(s, "%Y-%m-%d")

    def _check_with_registration(self, field, value):

        type_reg = self.document.get("type_registration")

        value = "".join(re.findall(r'\d', value))

        if not value:
            self._error(field, "empty values not allowed")
            return

        if type_reg == 1:

            if not validate_cpf(value):
                self._error(field, "Valid cpf required")
                return

        if type_reg == 2:

            if not validate_cnpj(value):
                self._error(field, "Valid cnpj required")

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

    def _check_with_payment_method(self, field, value):

        form = self.document.get("payment_form")

        if value > 1 and form == 1:
            self._error(
                field, "Número de parcelas para pagemento à vista não pode ser maior que 1")

    def _normalize_coerce_form_date(self, value):
        return to_date(value)

    def _validate_description(self, description, field, value):
        """ Insert Description for swagger.
        The rule's arguments are validated against this schema:
        {'type': 'string'}
        """
        return
