class Classifier:
  def __init__(self, trad, simp, pinyin):
    self.trad = trad
    self.simp = simp
    self.pinyin = pinyin

  @classmethod
  def parse(cls, s):
    if '|' in s:
      trad, rest = s.split('|')
      simp, pinyin = rest.split('[')
    else:
      trad = s
      simp = s
      simp, pinyin = s.split('[')
    pinyin = pinyin.rstrip(']')
    return cls(trad, simp, pinyin)