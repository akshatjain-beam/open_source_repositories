```
    def kana2mora(self, txt : str) -> List[str]:
        """
        - The `kana2mora` function converts a Japanese string (hiragana/katakana) into a list of morae (syllable units).
        - Non-Japanese characters or symbols are separated and returned as individual characters.
        - It adds `[BOS]` (start) and `[EOS]` (end) tokens to handle edge cases.
        - Iterates through consecutive character pairs using `check_if_successive_2chars_compose_mora` to form morae.
        - Filters out the `[BOS]` and `[EOS]` tokens and returns the list of morae.
        - Args: a string of Japanese text (hiragana or katakana).
        - Returns: a list of morae.
        """
        txt_with_bos_eos = "[BOS]" + txt + "[EOS]"
        morae = []
        for i in range(len(txt_with_bos_eos)-1):
            morae += self.check_if_successive_2chars_compose_mora(txt_with_bos_eos[i], txt_with_bos_eos[i+1])
        morae = list(filter(lambda x: x != "[BOS]" and x != "[EOS]", morae))
        return morae
```