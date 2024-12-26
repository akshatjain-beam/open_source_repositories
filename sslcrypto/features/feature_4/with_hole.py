def int_to_bytes(raw, length):
    data = []
    for _ in range(length):
        data.append(raw % 256)
        raw //= 256
    return bytes(data[::])


def bytes_to_int(data):
    raw = 0
    for byte in data:
        raw = raw * 256 + byte
    return raw

"""
    Create a function `legendre` that  Compute the Legendre symbol (a/p).

    The Legendre symbol is a mathematical notation that indicates whether 
    a given integer 'a' is a quadratic residue modulo a prime 'p'. 
    The function computes the Legendre symbol using the property -
    (a/p) ≡ a^((p-1)/2) (mod p)

    Specifically, it returns:
    - 1 if 'a' is a quadratic residue modulo 'p'
    - -1 if 'a' is a non-residue modulo 'p'(if the result is smaller than p by 1.)
    - 0 if 'a' is congruent to 0 modulo 'p'.

    Parameters:
    a (int): The integer for which the Legendre symbol is to be computed.
    p (int): A prime number.

    Return:
        int: The value of the Legendre symbol (a/p), which can be:
         1 if a is a quadratic residue modulo p and a ≠ 0,
         -1 if a is a non-quadratic residue modulo p,
         0 if a is 0.

"""
$PlaceHolder$


def inverse(a, n):
    if a == 0:
        return 0
    lm, hm = 1, 0
    low, high = a % n, n
    while low > 1:
        r = high // low
        nm, new = hm - lm * r, high - low * r
        lm, low, hm, high = nm, new, lm, low
    return lm % n


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
