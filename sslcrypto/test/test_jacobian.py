import unittest
from sslcrypto.fallback._util import legendre

class TestLegendreSymbol(unittest.TestCase):
    
    def test_quadratic_residue(self):
        """ 
        Test cases where the integer 'a' is a quadratic residue 
        modulo a prime 'p'. The expected result is 1 for these cases.
        
        """
        self.assertEqual(legendre(1, 7), 1)  
        self.assertEqual(legendre(2, 7), 1)  
        self.assertEqual(legendre(4, 7), 1)  
        self.assertEqual(legendre(9, 11), 1)

    def test_non_quadratic_residue(self):
        """ 
        Test cases where the integer 'a' is not a quadratic residue 
        modulo a prime 'p'. The expected result is -1 for these cases.
 
        """
        self.assertEqual(legendre(3, 7), -1) 
        self.assertEqual(legendre(5, 7), -1) 
        self.assertEqual(legendre(10, 11), -1)

    def test_zero_case(self):
        """ 
        Test cases where the integer 'a' is zero. The Legendre symbol 
        for zero modulo any prime 'p' should return 0.
        
        """
        self.assertEqual(legendre(0, 7), 0)  
        self.assertEqual(legendre(0, 11), 0) 

    def test_prime_cases(self):
        """ 
        Test cases for small prime numbers. This includes checks for 
        both quadratic residues and non-residues.
        
        """
        self.assertEqual(legendre(1, 2), -1)  
        self.assertEqual(legendre(2, 3), -1) 

    def test_large_prime_case(self):
        """ 
        Test cases using a larger prime number to verify correct 
        computation of Legendre symbols for both quadratic residues 
        and non-residues.
        
        """
        self.assertEqual(legendre(7, 19), 1)  
        self.assertEqual(legendre(8, 19), -1) 

if __name__ == '__main__':
    unittest.main()
