```
    def convert_lst_of_mora(self, lst : List[str], output_format="katakana", phoneme=False) -> List[str]:
        """
        Convert a list of morae into a list of katakana or hiragana or other formats.

        Args:
            lst (list): A list of morae.
            output_format (str): The output format of the morae. Defaults to "katakana".
                Options are ["katakana", "hiragana"], and any of the columns in the kanamap.csv file,
                including ["kunrei", "hepburn", "simple-ipa"]. Defaults to "katakana".
        """

        if output_format == "hiragana":
            map_f = lambda _ : k2h(_) if _ in self.kanamap.lst_katakana() else _
            ret = list(map(map_f, lst))
        elif output_format == "katakana":
            map_f = lambda _ : h2k(_) if _ in self.kanamap.lst_katakana() else _
            ret = list(map(map_f, lst))
        elif output_format in self.kanamap.header():
            map_f = lambda _ : self.kanamap(_)[output_format] if _ in self.kanamap.lst_katakana() else _
            morae = list(map(map_f, map(h2k, lst)))
            if output_format != "simple-ipa":
                morae = self.modify_special_mora(morae)
            if phoneme:
                morae = list("".join(morae))
            ret = morae
        else:
            raise ValueError(f"output_format {output_format} is not supported.")
        return ret
```