```
    def check_hashes(self, word_list: list):
        """
        Logs the duplicate hashed indices for words in words_list

        :param word_list: List of words
        :returns: set of indices
        """
        faulty_words = set()
        for w in word_list:
            indices = self.get_hashes(w)
            print(indices)
            res = Hash_Funcs.check_duplicates(indices)
            if res and res[1] not in faulty_words:
                faulty_words.add(res[1])
        return faulty_words
```