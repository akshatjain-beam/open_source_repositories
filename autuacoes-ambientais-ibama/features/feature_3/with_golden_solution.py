```
def cnpj_checks(text):
    check_1 = sum(int(c) * m for c, m in zip(text[:12], CNPJ_MULTIPLIERS_1)) % 11
    check_1 = str(11 - check_1 if check_1 >= 2 else 0)
    check_2 = sum(int(c) * m for c, m in zip(text[:12] + check_1, CNPJ_MULTIPLIERS_2)) % 11
    check_2 = str(11 - check_2 if check_2 >= 2 else 0)
    return check_1 + check_2
```