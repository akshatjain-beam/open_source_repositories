import unittest
import mmh3
from unittest.mock import MagicMock, patch
from sthir.spectral_bloom_filter import Hash_Funcs, Spectral_Bloom_Filter


class Test_Hashing(unittest.TestCase):
    def test_hashes1(self):
        """
        Test the hash function with a specific input 'dogs'.
        This test initializes a Hash_Funcs instance with k=3 and m=200,
        and checks if the returned list of hashes for the input string 'dogs'
        matches the expected output [133, 193, 69].
        """
        k, m = 3, 200
        hash_obj = Hash_Funcs(k, m)
        self.assertEqual([133, 193, 69],  hash_obj.get_hashes("dogs"))

    def test_hashes2(self):
        """
        Test the hash function with a specific input 'cats'.
        This test initializes a Hash_Funcs instance with k=5 and m=100,
        and checks if the returned list of hashes for the input string 'cats'
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


if __name__ == '__main__':
    unittest.main()

    # SBF = Spectral_Bloom_Filter()

    # print( )
