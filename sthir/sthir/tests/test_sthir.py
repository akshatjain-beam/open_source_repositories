import unittest
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
