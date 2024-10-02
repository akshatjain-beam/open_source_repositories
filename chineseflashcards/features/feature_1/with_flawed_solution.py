```
class Classifier:
  def __init__(self, trad, simp, pinyin):
    self.trad = trad
    self.simp = simp
    self.pinyin = pinyin

  @classmethod
  def parse(cls, s):
    if '|' in s:
      trad, rest = s.split('|', 1)
      simp, pinyin = rest.split('[', 1)
    else:
      trad = s.split('[', 1)[0]
      simp = trad
      pinyin = s.split('[', 1)[1]

    pinyin = pinyin.rstrip(']')

    return cls(trad, simp, pinyin)
```