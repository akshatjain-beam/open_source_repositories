```
def square_root_mod_prime(n, p):
    """Computes the modular square root of a number n modulo a prime p.

    This function finds an integer r such that r^2 ≡ n (mod p), assuming n is a quadratic residue modulo p.

    Parameters:
    n (int): The integer whose modular square root is to be calculated.
    p (int): A prime number representing the modulus.

    Returns:
    int: The modular square root of n modulo p. 
    Raises:
    ValueError: If n is not a quadratic residue modulo p or if an unexpected condition is encountered during computation.

    Implementation Steps:
    1. Check if n is zero. If it is, return 0 immediately since the square root of 0 is 0.
    2. Handle the case where p is 2, returning n directly.
    3. Check if the Legendre symbol (n/p) is equal to 1, indicating that n has a square root modulo p. 
        If not, raise a ValueError stating that no square root exists.
    4. For primes p that are congruent to 3 modulo 4, calculate the square root directly using the formula r ≡ n^{(p + 1) / 4} mod p.
    5. Factor out powers of 2 from p - 1 to express it as Q × 2^S where Q is odd.
        This is done by repeatedly dividing p - 1 by 2 until it is odd, counting the number of divisions as S and the resulting odd number as Q.
    6. Find a quadratic non-residue z in ℤ/pℤ (the integers modulo p).
        Start with z = 1 and increment z until you find the smallest integer for which the Legendre symbol (z/p) equals -1, indicating that z is a quadratic non-residue.
    7. Initialize variables m, c, t, and r as follows:
        - m: The exponent of 2 obtained from step 5.
        - c: A quadratic non-residue modulo p raised to the power of Q.
        - t: The value of n raised to the power of Q modulo p.
        - r: The initial candidate for the square root of n, calculated as n^{(Q + 1) / 2} mod p.
    8. Enter a loop that continues until specific conditions are met:
        - If t is 0, return 0, indicating that n is congruent to 0 modulo p.
        - If t is 1, return r, indicating a valid square root has been found.
        - Use repeated squaring to find the smallest integer i such that t^{(2^i)} ≡ 1 mod p.
        - If no such i is found, raise a ValueError.
    9. Update variables accordingly:
        - Set m to i, the index found.
        - Update c to b^2 modulo p.
        - Update t to the product of t and b^2 modulo p.
        - Update r to the product of r and b modulo p.
    10. Return the value of r as the modular square root of n modulo p.
    """
    if n == 0:
        return 0
    if p == 2:
        return n

    if legendre(n, p) != 1:
        raise ValueError("No square root exists.")

    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)

    Q = p - 1
    S = 0
    while Q % 2 == 0:
        Q //= 2
        S += 1

    z = 1
    while legendre(z, p) != -1:
        z += 1

    m = S
    c = pow(z, Q, p)
    t = pow(n, Q, p)
    r = pow(n, (Q + 1) // 2, p)

    while True:
        if t == 0:
            return 0
        if t == 1:
            return r

        i = 1
        while pow(t, pow(2, i), p) != 1:
            i += 1
        if i == m:
            raise ValueError("Unexpected condition.")
        m = i
        b = pow(c, pow(2, m - 1), p)
        c = pow(b, 2, p)
        t = (t * c) % p
        r = (r * b) % p

    return r
```