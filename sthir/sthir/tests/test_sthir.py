import unittest
from sthir.generate_search import base2p15_decode, base2p15_encode
from sthir.spectral_bloom_filter import Hash_Funcs, Spectral_Bloom_Filter


class Test_Hashing(unittest.TestCase):
    def test_hashes1(self):
        k, m = 3, 200
        hash_obj = Hash_Funcs(k, m)
        self.assertEqual([133, 193, 69],  hash_obj.get_hashes("dogs"))

    def test_hashes2(self):
        k, m = 5, 100
        hash_obj = Hash_Funcs(k, m)
        self.assertEqual([66, 78, 4, 86, 26],   hash_obj.get_hashes("cats"))


class Test_SBF(unittest.TestCase):
    def test_SBF(self):
        SBF = Spectral_Bloom_Filter()

        expected = (480, 3)
        actual = SBF.optimal_m_k(100, 0.1)
        self.assertEqual(expected,  actual)


class TestBase2p15Decode(unittest.TestCase):
    def test_basic_decoding(self):
        # Testing a basic example
        binary_str = '00001001'  # example binary string
        # encode to get base2p15 representation
        base2p15 = base2p15_encode(binary_str)
        result = base2p15_decode(base2p15)
        self.assertEqual(result, binary_str)

    def test_padding(self):
        # Test with a string that has padding
        binary_str = '110100111011001'  # example binary string with padding
        base2p15 = base2p15_encode(binary_str)
        result = base2p15_decode(base2p15)
        self.assertEqual(result, binary_str)

    def test_large_binary_string(self):
        # Test with a large binary string
        binary_str = '1' * 45  # 45 bits, more than 3 chunks of 15 bits
        base2p15 = base2p15_encode(binary_str)
        result = base2p15_decode(base2p15)
        self.assertEqual(result, binary_str)

    def test_partial_segment(self):
        # Test where the last segment is less than 15 bits
        binary_str = '111000'  # 6 bits
        base2p15 = base2p15_encode(binary_str)
        result = base2p15_decode(base2p15)
        self.assertEqual(result, binary_str)

    def test_edge_case_non_ascii_character(self):
        # Edge case: non-ASCII characters
        binary_str = '0000010000100010'  # binary string for '...' in non-printable ASCII
        base2p15 = base2p15_encode(binary_str)
        result = base2p15_decode(base2p15)
        self.assertEqual(result, binary_str)

    def test_edge_case_invalid_padding(self):
        # Edge case: invalid padding value
        binary_str = '11110000'  # some binary string with padding
        base2p15 = base2p15_encode(binary_str)
        result = base2p15_decode(base2p15)
        self.assertEqual(result, binary_str)


if __name__ == '__main__':
    unittest.main()

    # SBF = Spectral_Bloom_Filter()

    # print( )
