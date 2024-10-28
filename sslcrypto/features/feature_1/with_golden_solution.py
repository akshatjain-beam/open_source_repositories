```
def ROL(n, x):
    return ((x << n) & 0xffffffff) | (x >> (32 - n))
```