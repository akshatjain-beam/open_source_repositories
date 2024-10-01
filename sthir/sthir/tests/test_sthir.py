import unittest
from sthir.generate_search import base2p15_decode, base2p15_encode
from sthir.spectral_bloom_filter import Hash_Funcs, Spectral_Bloom_Filter


class Test_Hashing(unittest.TestCase):
    def test_hashes1(self):
        """
        Test the hash function with a specific input 'dogs'.
        This test initializes a Hash_Funcs instance with k=3 and m=200, and 
        checks if the returned list of hashes for the input string 'dogs'
        matches the expected output [133, 193, 69].
        """
        k, m = 3, 200
        hash_obj = Hash_Funcs(k, m)
        self.assertEqual([133, 193, 69],  hash_obj.get_hashes("dogs"))

    def test_hashes2(self):
        """
        Test the hash function with a specific input 'cats'.
        This test initializes a Hash_Funcs instance with k=5 and m=100, and 
        checks if the returned list of hashes for the input string 'cats'
        matches the expected output [66, 78, 4, 86, 26].
        """
        k, m = 5, 100
        hash_obj = Hash_Funcs(k, m)
        self.assertEqual([66, 78, 4, 86, 26],   hash_obj.get_hashes("cats"))


class Test_SBF(unittest.TestCase):
    def test_SBF(self):
        """
        Test the optimal parameters for a Spectral Bloom Filter.
        This test creates an instance of Spectral_Bloom_Filter and calls 
        the optimal_m_k method with a size of 100 and a false positive rate of 0.1. 
        It checks if the returned optimal parameters (m, k) match the expected values (480, 3).
        """
        SBF = Spectral_Bloom_Filter()

        expected = (480, 3)
        actual = SBF.optimal_m_k(100, 0.1)
        self.assertEqual(expected,  actual)


class TestBase2p15Decode(unittest.TestCase):
    def test_basic_decoding(self):
        """
        Test basic decoding functionality.
        This test encodes a simple binary string '00001001' into its base2p15 representation 
        and then decodes it back to verify that the original binary string is correctly recovered.
        """
        # Testing a basic example
        binary_str = '00001001'  # example binary string
        # encode to get base2p15 representation
        base2p15 = base2p15_encode(binary_str)
        result = base2p15_decode(base2p15)
        self.assertEqual(result, binary_str)

    def test_padding(self):
        """
        Test decoding with padding.
        This test encodes a binary string '110100111011001' that includes padding into its base2p15 
        representation and then decodes it back to verify that the original 
        binary string with padding is correctly recovered.
        """
        # Test with a string that has padding
        binary_str = '110100111011001'  # example binary string with padding
        base2p15 = base2p15_encode(binary_str)
        result = base2p15_decode(base2p15)
        self.assertEqual(result, binary_str)

    def test_large_binary_string(self):
        """
        Test decoding of a large binary string.
        This test encodes a large binary string of 45 bits into its base2p15 representation 
        and then decodes it back to verify that the original binary string is correctly recovered.
        """
        # Test with a large binary string
        binary_str = '1' * 45  # 45 bits, more than 3 chunks of 15 bits
        base2p15 = base2p15_encode(binary_str)
        result = base2p15_decode(base2p15)
        self.assertEqual(result, binary_str)

    def test_partial_segment(self):
        """
        Test decoding where the last segment is less than 15 bits.
        This test encodes a binary string '111000' with only 6 bits into its base2p15 representation 
        and then decodes it back to verify that the original short binary string is correctly recovered.
        """
        # Test where the last segment is less than 15 bits
        binary_str = '111000'  # 6 bits
        base2p15 = base2p15_encode(binary_str)
        result = base2p15_decode(base2p15)
        self.assertEqual(result, binary_str)

    def test_edge_case_non_ascii_character(self):
        """
        Test decoding of a binary string representing non-ASCII characters.
        This test encodes a binary string '0000010000100010', representing non-printable ASCII characters, 
        into its base2p15 representation and then decodes it back 
        to verify correct recovery of the original string.
        """
        # Edge case: non-ASCII characters
        binary_str = '0000010000100010'  # binary string for '...' in non-printable ASCII
        base2p15 = base2p15_encode(binary_str)
        result = base2p15_decode(base2p15)
        self.assertEqual(result, binary_str)

    def test_edge_case_invalid_padding(self):
        """
        Test decoding with an invalid padding value.
        This test encodes a binary string '11110000' with padding into its base2p15 representation 
        and then decodes it back to verify that the original binary string with padding is correctly recovered, 
        even with potential padding errors.
        """
        # Edge case: invalid padding value
        binary_str = '11110000'  # some binary string with padding
        base2p15 = base2p15_encode(binary_str)
        result = base2p15_decode(base2p15)
        self.assertEqual(result, binary_str)


if __name__ == '__main__':
    unittest.main()

    # SBF = Spectral_Bloom_Filter()

    # print( )
