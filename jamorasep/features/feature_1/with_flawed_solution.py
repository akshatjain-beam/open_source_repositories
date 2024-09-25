```
    def convert_lst_of_mora(self, lst : List[str], output_format : str = "katakana", phoneme : bool = False) -> List[str]:
        if output_format == "hiragana":
            result = [k2h(self.kanamap[mora]["hiragana"]) if mora in self.kanamap else mora for mora in lst]
        elif output_format == "katakana":
            result = [self.kanamap[mora]["katakana"] if mora in self.kanamap else mora for mora in lst]
        elif output_format in self.kanamap.header():
            result = [self.kanamap[mora][output_format] if mora in self.kanamap else mora for mora in lst]
            if output_format != "simple-ipa":
                result = self.modify_special_mora(result)
            if phoneme:
                result = "".join(result)
                result = list(result)
        else:
            raise ValueError(f"Invalid output format: {output_format}")
        return result
```