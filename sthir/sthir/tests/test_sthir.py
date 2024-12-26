import unittest
import mmh3
from unittest.mock import MagicMock, patch
from sthir.generate_search import base2p15_decode, base2p15_encode
from sthir.generate_search import gen_chunks
from unittest.mock import mock_open, patch, MagicMock
from bitarray import bitarray
from sthir.convert_2p15 import process_documents
from sthir.generate_search import base2p15_encode
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
        self.assertEqual([133, 193, 69], hash_obj.get_hashes("dogs"))

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

    @patch.object(Hash_Funcs, 'get_hashes')
    def test_check_hashes_with_duplicates(self, mock_get_hashes):
        """
        Test checking hashes with duplicate indices.
        This test mocks the get_hashes method to return indices that contain 
        duplicates for the word "apple". It verifies that the check_hashes 
        method correctly identifies index 1 as duplicated.
        """
        k, m = 3, 10
        hash_obj = Hash_Funcs(k, m)

        # Mock the get_hashes method to return specific indices
        def mock_get_hashes(word):
            if word == "apple":
                return [1, 2, 1]  # Duplicate index 1
            elif word == "banana":
                return [4, 5, 6]
            return []

        hash_obj.get_hashes = mock_get_hashes

        word_list = ["apple", "banana", "apple"]
        result = hash_obj.check_hashes(word_list)
        print(f"test_check_hashes_with_duplicates result: {result}")
        self.assertEqual(result, {1})  # Index 1 is duplicated

    @patch.object(Hash_Funcs, 'get_hashes')
    def test_check_hashes_no_duplicates(self, mock_get_hashes):
        """
        Test checking hashes with no duplicate indices.
        This test mocks the get_hashes method to return unique indices for 
        the words "apple", "banana", and "cherry". It verifies that the 
        check_hashes method returns an empty set, indicating no duplicates.
        """
        k, m = 3, 10
        hash_obj = Hash_Funcs(k, m)

        # Mock the get_hashes method to return unique indices
        def mock_get_hashes(word):
            if word == "apple":
                return [1, 2, 3]
            elif word == "banana":
                return [4, 5, 6]
            elif word == "cherry":
                return [7, 8, 9]
            return []

        hash_obj.get_hashes = mock_get_hashes

        word_list = ["apple", "banana", "cherry"]
        result = hash_obj.check_hashes(word_list)
        print(f"test_check_hashes_no_duplicates result: {result}")
        self.assertEqual(result, set())  # No duplicates expected

    @patch.object(Hash_Funcs, 'get_hashes')
    def test_check_hashes_empty_list(self, mock_get_hashes):
        """
        Test checking hashes with an empty list.
        This test checks that when an empty list is provided to the 
        check_hashes method, the result is an empty set, indicating 
        there are no words to check for duplicates.
        """
        k, m = 3, 10
        hash_obj = Hash_Funcs(k, m)

        # Mock is irrelevant here since list is empty
        hash_obj.get_hashes = mock_get_hashes

        word_list = []
        result = hash_obj.check_hashes(word_list)
        print(f"test_check_hashes_empty_list result: {result}")
        self.assertEqual(result, set())  # No duplicates expected

    @patch.object(Hash_Funcs, 'get_hashes')
    def test_check_hashes_single_word(self, mock_get_hashes):
        """
        Test checking hashes with a single word.
        This test mocks the get_hashes method to return unique indices 
        for the word "apple". It verifies that the check_hashes method 
        returns an empty set, indicating there are no duplicates for the 
        single word.
        """
        k, m = 3, 10
        hash_obj = Hash_Funcs(k, m)

        # Mock the get_hashes method to return specific indices
        def mock_get_hashes(word):
            if word == "apple":
                return [1, 2, 3]
            return []

        hash_obj.get_hashes = mock_get_hashes

        word_list = ["apple"]
        result = hash_obj.check_hashes(word_list)
        print(f"test_check_hashes_single_word result: {result}")
        self.assertEqual(result, set())  # No duplicates expected

    @patch.object(Hash_Funcs, 'get_hashes')
    def test_check_hashes_multiple_duplicates(self, mock_get_hashes):
        """
        Test checking hashes with multiple duplicate indices.
        This test mocks the get_hashes method to return indices that cause 
        collisions for the words "apple" and "banana". It verifies that 
        the check_hashes method correctly identifies index 1 as duplicated.
        """
        k, m = 3, 10
        hash_obj = Hash_Funcs(k, m)

        # Mock the get_hashes method to return indices that cause collisions
        def mock_get_hashes(word):
            if word == "apple":
                return [1, 2, 1]  # Duplicate index 1
            elif word == "banana":
                return [1, 3, 4]  # Duplicate index 1
            elif word == "cherry":
                return [5, 6, 7]
            return []

        hash_obj.get_hashes = mock_get_hashes

        word_list = ["apple", "banana", "cherry"]
        result = hash_obj.check_hashes(word_list)
        print(f"test_check_hashes_multiple_duplicates result: {result}")
        self.assertEqual(result, {1})  # Index 1 is duplicated

    @patch.object(Hash_Funcs, 'get_hashes')
    def test_check_hashes_same_hash_different_words(self, mock_get_hashes):
        """
        Test checking hashes where different words have the same hash.
        This test mocks the get_hashes method to return the same index 
        for all words. It verifies that the check_hashes method identifies 
        that index 1 is duplicated for multiple different words.
        """
        k, m = 3, 10
        hash_obj = Hash_Funcs(k, m)

        # Mock the get_hashes method to return the same hash for different words
        def mock_get_hashes(word):
            return [1, 1, 1]  # All indices are the same

        hash_obj.get_hashes = mock_get_hashes

        word_list = ["apple", "banana", "cherry"]
        result = hash_obj.check_hashes(word_list)
        print(f"test_check_hashes_same_hash_different_words result: {result}")
        self.assertEqual(result, {1})  # Index 1 is duplicated
        self.assertEqual([66, 78, 4, 86, 26], hash_obj.get_hashes("cats"))


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
class TestGenChunks(unittest.TestCase):
    def test_standard_chunks(self):
        self.assertEqual(list(gen_chunks('123456789A', 4)),
                         ['1234', '5678', '9A'])

    def test_standard_chunks_with_remainder_dropped(self):
        self.assertEqual(
            list(gen_chunks('123456789A', 4, drop_remaining=True)), ['1234', '5678'])

    def test_exact_chunks(self):
        self.assertEqual(list(gen_chunks('12345678', 4)), ['1234', '5678'])

    def test_exact_chunks_with_remainder_dropped(self):
        self.assertEqual(
            list(gen_chunks('12345678', 4, drop_remaining=True)), ['1234', '5678'])

    def test_chunk_size_larger_than_string(self):
        self.assertEqual(list(gen_chunks('123', 5)), ['123'])

    def test_chunk_size_larger_than_string_with_remainder_dropped(self):
        self.assertEqual(list(gen_chunks('123', 5, drop_remaining=True)), [])

    def test_chunk_size_one(self):
        self.assertEqual(list(gen_chunks('123456789A', 1)), [
                         '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A'])

    def test_empty_string(self):
        self.assertEqual(list(gen_chunks('', 4)), [])

    def test_chunk_size_zero(self):
        with self.assertRaises(ValueError):
            list(gen_chunks('123456789A', 0))

    def test_non_string_input(self):
        with self.assertRaises(TypeError):
            list(gen_chunks(123456789, 4))
class TestDocumentProcessing(unittest.TestCase):

    @patch('sthir.convert_2p15.open', new_callable=mock_open, read_data=b'\x01\x02\x03\x04')
    def test_document_processing(self, mock_open):
        """
        Test document processing with a valid binary file.

        This test simulates reading a binary file containing specific bytes. It 
        mocks the bitarray instance and its methods to return a predetermined 
        binary string. The test checks that the processed output matches the 
        expected list after encoding the binary data and preserving the document metadata.
        """
        # Mocking the bitarray instance and its methods
        mock_bitarray = MagicMock(spec=bitarray)
        mock_bitarray.to01.return_value = '00000001000000100000001100000100'

        with patch('bitarray.bitarray', return_value=mock_bitarray):
            # Prepare test data
            documents = [["document.bin", 4, 14474, 3], [
                "A simple way to get more value from metrics.bin", 4, 11086, 3]]

            # Expected results after encoding
            expected_base2p15_arrs = [
                [base2p15_encode('00000001000000100000001100000100'),
                 4, 14474, 3, "document.bin"],
                [base2p15_encode('00000001000000100000001100000100'), 4, 11086,
                 3, "A simple way to get more value from metrics.bin"]
            ]

            # Run the code
            base2p15_arrs = process_documents(documents)

            # Verify the results
            self.assertEqual(base2p15_arrs, expected_base2p15_arrs)

    @patch('sthir.convert_2p15.open', new_callable=mock_open, read_data=b'')
    def test_document_processing_empty_file(self, mock_open):
        """
        Test document processing with an empty binary file.

        This test simulates reading an empty binary file. It mocks the bitarray
        instance and its methods to return an empty string. The test checks that
        the processed output matches the expected list, which should include the 
        base2p15 encoding of an empty string followed by the document metadata.
        """
        # Mocking the bitarray instance and its methods
        mock_bitarray = MagicMock(spec=bitarray)
        mock_bitarray.to01.return_value = ''

        with patch('bitarray.bitarray', return_value=mock_bitarray):
            # Prepare test data
            documents = [["empty.bin", 4, 14474, 3]]

            # Expected results after encoding
            expected_base2p15_arrs = [
                [base2p15_encode(''), 4, 14474, 3, "empty.bin"]
            ]

            # Run the code
            base2p15_arrs = process_documents(documents)

            # Verify the results
            self.assertEqual(base2p15_arrs, expected_base2p15_arrs)

    @patch('sthir.convert_2p15.open', new_callable=mock_open)
    def test_document_processing_invalid_file(self, mock_open):
        """
        Test document processing with an invalid binary file.

        This test simulates a scenario where reading from a binary file fails. 
        It mocks the bitarray instance to raise an exception when trying to read the file. 
        The test ensures that the process_documents function raises an exception as expected.
        """
        # Mocking the bitarray instance and its methods to raise an exception
        mock_bitarray = MagicMock(spec=bitarray)
        mock_bitarray.fromfile.side_effect = Exception('File read error')

        with patch('bitarray.bitarray', return_value=mock_bitarray):
            # Prepare test data
            documents = [["invalid.bin", 4, 14474, 3]]

            # Run the code and check for exception
            with self.assertRaises(Exception):
                process_documents(documents)

    # Simulating a 10 MB file
    @patch('sthir.convert_2p15.open', new_callable=mock_open, read_data=b'\x00' * 1024 * 1024 * 10)
    def test_document_processing_large_file(self, mock_open):
        """
        Test document processing with a large binary file.

        This test simulates reading a large binary file (10 MB of zero bytes). 
        It mocks the bitarray instance to return a long binary string of zeroes. 
        The test checks that the processed output matches the expected list, 
        which should include the base2p15 encoding of a large string of zeroes 
        followed by the document metadata.
        """
        # Mocking the bitarray instance and its methods
        mock_bitarray = MagicMock(spec=bitarray)
        mock_bitarray.to01.return_value = '0' * \
            (1024 * 1024 * 10 * 8)  # Simulating a large bit array

        with patch('bitarray.bitarray', return_value=mock_bitarray):
            # Prepare test data
            documents = [["large_file.bin", 4, 14474, 3]]

            # Expected results after encoding
            expected_base2p15_arrs = [
                [base2p15_encode('0' * (1024 * 1024 * 10 * 8)),
                 4, 14474, 3, "large_file.bin"]
            ]

            # Run the code
            base2p15_arrs = process_documents(documents)

            # Verify the results
            self.assertEqual(base2p15_arrs, expected_base2p15_arrs)

    @patch('sthir.convert_2p15.open', new_callable=mock_open, read_data='This is not a binary file.')
    def test_document_processing_non_binary_file(self, mock_open):
        """
        Test document processing with a non-binary file.

        This test simulates trying to read a non-binary file. 
        It mocks the bitarray instance to raise an exception when attempting to read the file. 
        The test checks that the process_documents function raises an exception as expected.
        """
        # Mocking the bitarray instance and its methods to raise an exception
        mock_bitarray = MagicMock(spec=bitarray)
        mock_bitarray.fromfile.side_effect = Exception('File read error')

        with patch('bitarray.bitarray', return_value=mock_bitarray):
            # Prepare test data
            documents = [["non_binary.txt", 4, 14474, 3]]

            # Run the code and check for exception
            with self.assertRaises(Exception):
                process_documents(documents)


if __name__ == '__main__':
    unittest.main()

    # SBF = Spectral_Bloom_Filter()

    # print( )
