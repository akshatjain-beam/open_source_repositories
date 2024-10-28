```
def ROL(n, x):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF
```