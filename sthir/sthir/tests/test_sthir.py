import unittest
from sthir.generate_search import gen_chunks
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


if __name__ == '__main__':
    unittest.main()

    # SBF = Spectral_Bloom_Filter()

    # print( )
