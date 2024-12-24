```
    def check_hashes(self, word_list: list):
        faulty_words = set()
        for word in word_list:
            hashes = self.get_hashes(word)
            is_duplicate, _ = self.check_duplicates(hashes)
            if is_duplicate:
                faulty_words.add(word)
        return faulty_words
```