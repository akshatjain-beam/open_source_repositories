import re


INVALID_CPFS = tuple(str(i) * 11 for i in range(10))
CNPJ_MULTIPLIERS_1 = tuple(int(x) for x in "543298765432")
CNPJ_MULTIPLIERS_2 = tuple(int(x) for x in "6543298765432")
REGEXP_NUMBERS = re.compile("[0-9]")


def cpf_checks(text):
    """
    >>> cpf_checks("111111111xx")
    '11'

    >>> cpf_checks("123456789xx")
    '09'
    """
    check_1 = str(((sum(int(c) * (10 - i) for i, c in enumerate(text[:9])) * 10) % 11) % 10)
    check_2 = str(((sum(int(c) * (11 - i) for i, c in enumerate(text[:9] + check_1)) * 10) % 11) % 10)
    return check_1 + check_2


def is_valid_cpf(text):
    text = "".join(REGEXP_NUMBERS.findall(text)).strip()
    if not text.isdigit() or len(text) > 11:
        return False
    text = "0" * (11 - len(text)) + text
    if text in INVALID_CPFS:
        return False
    return cpf_checks(text) == text[-2:]

"""
    Create a function `cnpj_check` that calculates the checksum digits for a given CNPJ number.

    This function computes the two verification digits used in a Brazilian CNPJ 
    (Cadastro Nacional da Pessoa Jurídica) number. It utilizes the first 12 digits 
    of the CNPJ to compute the first check digit, and the first 13 digits (including 
    the first check digit) to compute the second check digit.

    The calculations are performed as follows:
    1. First Check Digit:
        - Multiply each of the first 12 digits by a specified multiplier in the order: 
          5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2. [Stored in CNPJ_MULTIPLIERS_1]
        - Sum these products and calculate the modulo 11 of the sum.
        - If the result is 0 or 1, the first check digit is 0; 
            - otherwise, subtract the result from 11 to get the first check digit.

    2. Second Check Digit:
        - Multiply each of the first 12 digits (plus the first check digit) by a specified multiplier in the order: 
          6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2. [Stored in CNPJ_MULTIPLIERS_2]
        - Sum these products and calculate the modulo 11 of the sum.
        - Again, if the result is 0 or 1, the second check digit is 0; 
            -otherwise, subtract the result from 11 to get the second check digit.

    Args:
        text (str): string of the CNPJ number, should contain at least 12 digits.

    Returns:
        str: string containing the two checksum digits.
"""
$PlaceHolder$

def is_valid_cnpj(text):
    text = "".join(REGEXP_NUMBERS.findall(text)).strip()
    if not text.isdigit() or len(text) > 14:
        return False
    text = "0" * (14 - len(text)) + text
    return cnpj_checks(text) == text[-2:]
