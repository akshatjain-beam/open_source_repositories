```
def cnpj_checks(text):
    check_1 = str(((sum(int(d) * m for d, m in zip(text[:12], CNPJ_MULTIPLIERS_1)) * 10) % 11) % 10)
    check_2 = str(((sum(int(d) * m for d, m in zip(text[:13], CNPJ_MULTIPLIERS_2)) * 10) % 11) % 10)
    return check_1 + check_2
```