# -*- coding: utf-8 -*-

from cerberus import Validator, TypeDefinition

from decimal import Decimal

decimal_type = TypeDefinition('decimal', (Decimal,), ())


class CustomValidator(Validator):

    types_mapping = Validator.types_mapping.copy()
    types_mapping['decimal'] = decimal_type
