import unittest
import mmh3
from unittest.mock import MagicMock, patch
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

    @patch.object(Hash_Funcs, 'get_hashes')
    def test_check_hashes_with_duplicates(self, mock_get_hashes):
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


class Test_SBF(unittest.TestCase):
    def test_SBF(self):
        SBF = Spectral_Bloom_Filter()

        expected = (480, 3)
        actual = SBF.optimal_m_k(100, 0.1)
        self.assertEqual(expected,  actual)


if __name__ == '__main__':
    unittest.main()

    # SBF = Spectral_Bloom_Filter()

    # print( )
