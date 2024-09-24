```
    def convert_lst_of_mora(self, lst : List[str], output_format : str = "katakana", phoneme : bool = False) -> List[str]:
        if output_format == "hiragana":
            return [k2h(mora) for mora in lst]
        elif output_format == "katakana":
            return [h2k(mora) for mora in lst]
        elif output_format in self.kanamap.header():
            result = []
            for mora in lst:
                if mora in self.kanamap.lst_katakana():
                    result.append(self.kanamap(mora)[output_format])
                else:
                    result.append(mora)

            if output_format != "simple-ipa":
                result = self.modify_special_mora(result)

            if phoneme:
                result = "".join(result)
                result = list(result)
            return result
        else:
            raise ValueError(f"Invalid output format: {output_format}")
```