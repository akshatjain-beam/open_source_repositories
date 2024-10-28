import unittest
from sslcrypto.fallback._jacobian import JacobianCurve

class TestJacobianCurve(unittest.TestCase):
    """
    Unit tests for the JacobianCurve class, covering essential operations on elliptic curves.
    
    These tests ensure that points on the elliptic curve are correctly identified, that the point at
    infinity behaves as expected, and that specific calculations like scalar multiplication are accurate.
    The tests also validate edge cases, such as handling of large coordinate values and negative coordinates.
    """

    def setUp(self):
        """
        Set up a sample JacobianCurve instance with typical parameters.

        Initializes a JacobianCurve with sample parameters, representing the secp256k1 elliptic curve, 
        including the prime modulus p, curve order n, curve parameters a and b, and the generator point g.
        """
        self.curve = JacobianCurve(
            p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
            n=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
            a=0,
            b=7,
            g=(55066263022277343669578718895168534326250603453777594175500187360389116729240,
               32670510020758816978083085130507043184471273380659243275938904335757337482424)
        )

    def test_point_on_curve(self):
        """
        Test a known valid point on the curve.
        
        Confirms that the generator point g lies on the curve by checking that it satisfies
        the elliptic curve equation. This is a basic validity check for points on the curve.
        """
        point = self.curve.g  # Generator point, assumed to be on the curve
        self.assertTrue(self.curve.is_on_curve(point))

    def test_point_off_curve(self):
        """
        Test a point that is not on the curve.
        
        Uses an arbitrary point (1, 2) that is not expected to satisfy the curve equation.
        Ensures that the curve recognizes points that are not part of the elliptic curve.
        """
        point = (1, 2)  # Arbitrary point not on the curve
        self.assertFalse(self.curve.is_on_curve(point))

    def test_point_at_infinity(self):
        """
        Test the point at infinity, represented as (0, 0) in affine coordinates.
        
        Verifies that the point at infinity, often used as an identity element in elliptic
        curve arithmetic, does not satisfy the curve equation in affine form.
        """
        point = (0, 0)
        self.assertFalse(self.curve.is_on_curve(point))

    def test_negative_coordinates(self):
        """
        Test with negative coordinates to ensure proper handling.
        
        Uses negative coordinates derived from the generator point g and verifies that
        they do not satisfy the curve equation, as curve points should be positive modulo p.
        """
        point = (-self.curve.g[0] % self.curve.p, -self.curve.g[1] % self.curve.p)
        self.assertFalse(self.curve.is_on_curve(point))

    def test_large_coordinates(self):
        """
        Test with large coordinates near the prime modulus boundary.
        
        Confirms that values near the curve’s prime modulus boundary do not satisfy
        the curve equation, ensuring that boundary conditions are handled correctly.
        """
        point = (self.curve.p - 1, self.curve.p - 2)
        self.assertFalse(self.curve.is_on_curve(point))

    def test_n_times_generator(self):
        """
        Test if n times the generator point results in the point at infinity.
        
        Verifies that scalar multiplication of the generator point by the curve order n
        yields the point at infinity, a property of elliptic curves.
        """
        n_times_g = self.curve.jacobian_multiply(self.curve.to_jacobian(self.curve.g), self.curve.n)
        self.assertTrue(self.curve.isinf(n_times_g))

if __name__ == '__main__':
    unittest.main()
