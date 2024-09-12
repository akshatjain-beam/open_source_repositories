class Classifier:
  def __init__(self, trad, simp, pinyin):
    self.trad = trad
    self.simp = simp
    self.pinyin = pinyin

  @classmethod
  def parse(cls, text):
    if '|' in text:
      trad, rest = text.split('|', 1)
      simp, pinyin = rest.split('[', 1)
    else:
      trad = text
      simp, pinyin = text.split('[', 1)
    pinyin = pinyin.rstrip(']')
    return cls(trad, simp, pinyin)