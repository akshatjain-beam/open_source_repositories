```
    def convert_lst_of_mora(self, lst : List[str], output_format : str = "katakana", phoneme : bool = False) -> List[str]:
        """
        Convert a list of morae into a different format.

        Args:
            lst (List[str]): A list of morae.
            output_format (str): The output format of the morae. Defaults to "katakana".
                Options are ["katakana", "hiragana"], and any of the columns in the kanamap.csv file,
                including ["kunrei", "hepburn", "simple-ipa"].
            phoneme (bool): If True, the output is a list of phonemes. Defaults to False.
                This flag is only valid when output_format is either of ["kunrei", "hepburn", "simple-ipa"].
        Returns:
            Union[List[str], str]: A list of morae in the specified format.
                If phoneme is True, the output is a single string of phonemes.
        Raises:
            ValueError: If the output format is invalid.
        """
        if output_format == "hiragana":
            return [k2h(m) if m in self.kanamap.lst_katakana() else m for m in lst]
        elif output_format == "katakana":
            return [h2k(m) if m in self.kanamap.lst_katakana() else m for m in lst]
        elif output_format in self.kanamap.header():
            res = [self.kanamap(h2k(m))[output_format] if m in self.kanamap.lst_katakana() else m for m in lst]
            if output_format != "simple-ipa":
                res = self.modify_special_mora(res)
            if phoneme:
                res = "".join(res)
            return res
        else:
            raise ValueError("Invalid output_format.")
```