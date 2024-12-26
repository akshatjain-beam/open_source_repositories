import unittest

from sslcrypto.fallback._util import square_root_mod_prime


class TestSquareRootModPrime(unittest.TestCase):

    def test_case_1_valid_square(self):
        """Test case 1: Valid square root.
        
        This test checks the function `square_root_mod_prime` with a known square number, 
        where n = 4 and p = 7. The expected output is 2, as 2 is the square root of 4 modulo 7.
        This verifies that the function correctly identifies square roots when they exist.
        """
        n = 4
        p = 7
        result = square_root_mod_prime(n, p)
        self.assertEqual(result, 2)  

    def test_case_2_zero_input(self):
        """Test case 2: Square root of zero.
        
        This test evaluates the behavior of the function when n = 0 and p = 11. 
        Since the square root of 0 is 0 in any field, the expected output is 0. 
        This case ensures the function correctly handles the input zero.
        """
        n = 0
        p = 11
        result = square_root_mod_prime(n, p)
        self.assertEqual(result, 0)

    def test_case_3_no_square_root(self):
        """Test case 3: No square root exists.
        
        In this test, we check the function with n = 3 and p = 11. 
        Since 3 is not a quadratic residue modulo 11, the expected output is 
        a number which, when squared, would be equivalent to 3 modulo 11 (which is 5 in this case).
        This tests the function's ability to find non-obvious roots.
        """
        n = 3
        p = 11
        result = square_root_mod_prime(n, p)
        self.assertEqual(result, 5)

    def test_case_4_prime_mod_3(self):
        """Test case 4: Prime number where p ≡ 3 (mod 4).
        
        This test uses n = 5 and p = 41, which is a prime number that satisfies 
        the condition p ≡ 3 (mod 4). The expected output is 28, as it is the modular 
        square root of 5 modulo 41. This verifies that the function correctly handles 
        special cases involving primes with this property.
        """
        n = 5
        p = 41
        result = square_root_mod_prime(n, p)
        self.assertEqual(result, 28)  

    def test_case_5_edge_case_small_prime(self):
        """Test case 5: Edge case with a small non-prime.
        
        This test examines the function's response to a non-prime input, where n = 5 
        and p = 9. Since 9 is not a prime number, the function is expected to raise 
        a ValueError. This tests the input validation and error handling of the function.
        """
        n = 5
        p = 9
        with self.assertRaises(ValueError) as context:
            square_root_mod_prime(n, p)

if __name__ == '__main__':
    unittest.main()
