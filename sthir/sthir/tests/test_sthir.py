import unittest
from sthir.generate_search import base2p15_encode
from sthir.spectral_bloom_filter import Hash_Funcs, Spectral_Bloom_Filter


class Test_Hashing(unittest.TestCase):
    def test_hashes1(self):
        """
        Test the Hash_Funcs class with k=3 and m=200.
        
        This test checks the correctness of the hash function by asserting that 
        the generated hashes for the input "dogs" match the expected output 
        [133, 193, 69].
        """
        k, m = 3, 200
        hash_obj = Hash_Funcs(k, m)
        self.assertEqual([133, 193, 69],  hash_obj.get_hashes("dogs"))

    def test_hashes2(self):
        """
        Test the Hash_Funcs class with k=5 and m=100.
        
        This test verifies that the hash function produces the expected output 
        [66, 78, 4, 86, 26] for the input "cats", ensuring the correctness 
        of multiple hash outputs.
        """
        k, m = 5, 100
        hash_obj = Hash_Funcs(k, m)
        self.assertEqual([66, 78, 4, 86, 26],   hash_obj.get_hashes("cats"))


class Test_SBF(unittest.TestCase):
    def test_SBF(self):
        """
        Test the Spectral_Bloom_Filter's optimal_m_k method.
        
        This test assesses whether the optimal parameters m and k can be computed 
        correctly for the given input of n=100 and false positive rate=0.1. 
        The expected output is (480, 3).
        """
        SBF = Spectral_Bloom_Filter()

        expected = (480, 3)
        actual = SBF.optimal_m_k(100, 0.1)
        self.assertEqual(expected,  actual)


class TestBase2p15Encode(unittest.TestCase):
    def test_empty_string(self):
        """
        Test encoding an empty string.
        
        This test checks that encoding an empty string returns '0', as no 
        bits are present to encode.
        """
        self.assertEqual(base2p15_encode(""), "0")

    def test_single_chunk(self):
        """
        Test encoding a string that is exactly 15 bits long.
        
        This test ensures that a 15-bit string is encoded correctly. 
        The expected output is '0\xa1', indicating no padding was required.
        """
        self.assertEqual(base2p15_encode("000000000000000"), "0\xa1")

    def test_padding(self):
        """
        Test encoding a string that requires padding.
        
        This test verifies that a 14-bit string correctly adds one padding bit,
        leading to the expected output of '1\xa1' after encoding.
        """
        self.assertEqual(base2p15_encode("00000000000000"), "1\xa1")
    
    def test_multiple_chunks(self):
        """
        Test encoding a string that results in multiple chunks.
        
        This test checks the encoding of a 45-bit string, which consists of 
        3 full chunks of 15 bits each. The expected output is '5' followed 
        by three instances of the character represented by 0xa1.
        """
        # Example: "0000000000000000000000000000000000000000" (45 bits)
        # 3 chunks of 15 bits, no padding
        encoded_chunks = chr(0xa1) * 3
        self.assertEqual(base2p15_encode("0000000000000000000000000000000000000000"), "5" + encoded_chunks)

    def test_non_multiple_of_15_bits(self):
        """
        Test encoding a string with a length that is not a multiple of 15.
        
        This test ensures that a 30-bit string, which requires padding of 1 
        bit to reach the next multiple of 15, is encoded correctly. The 
        expected output is '1\xa1\xa1'.
        """
        self.assertEqual(base2p15_encode(
            "00000000000000000000000000000"), "1\xa1\xa1")

    def test_edge_case_long_string(self):
        """
        Test encoding a very long string.
        
        This test evaluates the encoding of a 150-bit string. The expected 
        output should correctly reflect the number of chunks and any necessary 
        padding, producing the correct encoded string.
        """
        bit_string = "1" * 150  # 150 bits long
        expected_output = "0" + "".join(chr(0xa1 + int("1" * 15, 2)) * 10)
        self.assertEqual(base2p15_encode(bit_string), expected_output)

    def test_non_binary_characters(self):
        """
        Test encoding a string with non-binary characters.
        
        This test checks that the function raises a ValueError when 
        attempting to encode a string containing non-binary characters 
        """
        with self.assertRaises(ValueError):
            base2p15_encode("0000a0000000000")


if __name__ == '__main__':
    unittest.main()

    # SBF = Spectral_Bloom_Filter()

    # print( )
