import unittest
from unittest.mock import mock_open, patch, MagicMock
from bitarray import bitarray
from sthir.convert_2p15 import process_documents
from sthir.generate_search import base2p15_encode
from sthir.spectral_bloom_filter import Hash_Funcs, Spectral_Bloom_Filter


class Test_Hashing(unittest.TestCase):
    def test_hashes1(self):
        k, m = 3, 200
        hash_obj = Hash_Funcs(k, m)
        self.assertEqual([133, 193, 69], hash_obj.get_hashes("dogs"))

    def test_hashes2(self):
        k, m = 5, 100
        hash_obj = Hash_Funcs(k, m)
        self.assertEqual([66, 78, 4, 86, 26], hash_obj.get_hashes("cats"))


class Test_SBF(unittest.TestCase):
    def test_SBF(self):
        SBF = Spectral_Bloom_Filter()

        expected = (480, 3)
        actual = SBF.optimal_m_k(100, 0.1)
        self.assertEqual(expected,  actual)


class TestDocumentProcessing(unittest.TestCase):

    @patch('sthir.convert_2p15.open', new_callable=mock_open, read_data=b'\x01\x02\x03\x04')
    def test_document_processing(self, mock_open):
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
