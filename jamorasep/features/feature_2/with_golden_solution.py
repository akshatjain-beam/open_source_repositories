```
    def kana2mora(self, txt : str) -> List[str]:
        """
        Convert a string of Japanese text (hiragana or katakana) into a list of morae. (Mora is a unit of Japanese syllable.)
        Symbols and characters other than hiragana/katakana are just separated character-wise and returned without any modification.
        For example,
            "あいうえお・きゃきゅきょ・一二三<tag>"
        will be converted into
            ["あ", "い", "う", "え", "お", "・", "きゃ", "きゅ", "きょ", "・", "一", "二", "三", "<", "t", "a", "g", ">"]

        Args:
            a string of Japanese text (hiragana or katakana).
        Returns:
            a list of morae.
        """
        bos_token = "[BOS]"
        eos_token = "[EOS]"
        lst = [bos_token] + list(txt) + [eos_token]
        lst1, lst2 = lst[:-1], lst[1:]
        morae = [self.check_if_successive_2chars_compose_mora(*v) for v in zip(lst1, lst2)]
        morae = sum(morae, [])
        morae = list(filter(lambda x: x not in [bos_token, eos_token], morae))
        return morae
```