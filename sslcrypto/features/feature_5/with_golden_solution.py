```
def square_root_mod_prime(n, p):
    if n == 0:
        return 0
    if p == 2:
        return n  # We should never get here but it might be useful
    if legendre(n, p) != 1:
        raise ValueError("No square root")
    # Optimizations
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)
    # 1. By factoring out powers of 2, find Q and S such that p - 1 =
    # Q * 2 ** S with Q odd
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    # 2. Search for z in Z/pZ which is a quadratic non-residue
    z = 1
    while legendre(z, p) != -1:
        z += 1
    m, c, t, r = s, pow(z, q, p), pow(n, q, p), pow(n, (q + 1) // 2, p)
    while True:
        if t == 0:
            return 0
        elif t == 1:
            return r
        # Use repeated squaring to find the least i, 0 < i < M, such
        # that t ** (2 ** i) = 1
        t_sq = t
        i = 0
        for i in range(1, m):
            t_sq = t_sq * t_sq % p
            if t_sq == 1:
                break
        else:
            raise ValueError("Should never get here")
        # Let b = c ** (2 ** (m - i - 1))
        b = pow(c, 2 ** (m - i - 1), p)
        m = i
        c = b * b % p
        t = t * b * b % p
        r = r * b % p
    return r
```