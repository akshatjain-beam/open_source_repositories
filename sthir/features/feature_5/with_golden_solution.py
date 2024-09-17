```
        faulty_words = set()
        for w in word_list:
            indices = self.get_hashes(w)
            res = Hash_Funcs.check_duplicates(indices)
            if res and res[1] not in faulty_words:
                faulty_words.add(res[1])
        return faulty_words
```