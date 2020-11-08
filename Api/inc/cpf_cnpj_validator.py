#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

__all__ = ['validate_cpf', 'validate_cnpj']


def validate_cpf(cpf):
    """
    Valida CPFs, retornando apenas a string de números válida.

    # CPFs errados
    >>> validate_cpf('abcdefghijk')
    False
    >>> validate_cpf('123')
    False
    >>> validate_cpf('')
    False
    >>> validate_cpf(None)
    False
    >>> validate_cpf('12345678900')
    False

    # CPFs corretos
    >>> validate_cpf('95524361503')
    '95524361503'
    >>> validate_cpf('955.243.615-03')
    '95524361503'
    >>> validate_cpf('  955 243 615 03  ')
    '95524361503'
    """
    cpf = ''.join(re.findall(r'\d', str(cpf)))

    if (not cpf) or (len(cpf) < 11):
        return False

    # Pega apenas os 9 primeiros dígitos do CPF e gera os 2 dígitos que faltam
    inteiros = list(map(int, cpf))
    novo = inteiros[:9]

    while len(novo) < 11:
        r = sum([(len(novo)+1-i)*v for i, v in enumerate(novo)]) % 11

        if r > 1:
            f = 11 - r
        else:
            f = 0
        novo.append(f)

    # Se o número gerado coincidir com o número original, é válido
    if novo == inteiros:
        return cpf
    return False


def validate_cnpj(cnpj):
    """
    Valida CNPJs, retornando apenas a string de números válida.

    # CNPJs errados
    >>> validate_cnpj('abcdefghijklmn')
    False
    >>> validate_cnpj('123')
    False
    >>> validate_cnpj('')
    False
    >>> validate_cnpj(None)
    False
    >>> validate_cnpj('12345678901234')
    False
    >>> validate_cnpj('11222333000100')
    False

    # CNPJs corretos
    >>> validate_cnpj('11222333000181')
    '11222333000181'
    >>> validate_cnpj('11.222.333/0001-81')
    '11222333000181'
    >>> validate_cnpj('  11 222 333 0001 81  ')
    '11222333000181'
    """
    cnpj = ''.join(re.findall(r'\d', str(cnpj)))

    if (not cnpj) or (len(cnpj) < 14):
        return False

    # Pega apenas os 12 primeiros dígitos do CNPJ e gera os 2 dígitos que faltam
    inteiros = list(map(int, cnpj))
    novo = inteiros[:12]

    prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    while len(novo) < 14:
        r = sum([x*y for (x, y) in zip(novo, prod)]) % 11
        if r > 1:
            f = 11 - r
        else:
            f = 0
        novo.append(f)
        prod.insert(0, 6)

    # Se o número gerado coincidir com o número original, é válido
    if novo == inteiros:
        return cnpj
    return False
