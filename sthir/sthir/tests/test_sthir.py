import unittest
from sthir.generate_search import base2p15_encode
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


class TestBase2p15Encode(unittest.TestCase):
    def test_empty_string(self):
        """Test encoding an empty string."""
        self.assertEqual(base2p15_encode(""), "0")

    def test_single_chunk(self):
        """Test encoding a string that is exactly 15 bits long."""
        self.assertEqual(base2p15_encode("000000000000000"), "0\xa1")

    def test_padding(self):
        """Test encoding a string that requires padding."""
        self.assertEqual(base2p15_encode("00000000000000"), "1\xa1")
    
    def test_multiple_chunks(self):
        """Test encoding a string that results in multiple chunks."""
        # Example: "0000000000000000000000000000000000000000" (45 bits)
        # 3 chunks of 15 bits, no padding
        encoded_chunks = chr(0xa1) * 3
        self.assertEqual(base2p15_encode("0000000000000000000000000000000000000000"), "5" + encoded_chunks)

    def test_non_multiple_of_15_bits(self):
        """Test encoding a string with a length that is not a multiple of 15."""
        self.assertEqual(base2p15_encode(
            "00000000000000000000000000000"), "1\xa1\xa1")

    def test_edge_case_long_string(self):
        """Test encoding a very long string."""
        bit_string = "1" * 150  # 150 bits long
        expected_output = "0" + "".join(chr(0xa1 + int("1" * 15, 2)) * 10)
        self.assertEqual(base2p15_encode(bit_string), expected_output)

    def test_non_binary_characters(self):
        """Test encoding a string with non-binary characters (should raise an error)."""
        with self.assertRaises(ValueError):
            base2p15_encode("0000a0000000000")


if __name__ == '__main__':
    unittest.main()

    # SBF = Spectral_Bloom_Filter()

    # print( )
