class Classifier:
  def __init__(self, trad, simp, pinyin):
    self.trad = trad
    self.simp = simp
    self.pinyin = pinyin

  @classmethod
  def parse(cls, s):
    if '|' in s:
      trad, rest = s.split('|')
      simp, rest = rest.split('[')
    else:
      trad, rest = s.split('[')
      simp = trad
    pinyin = rest.rstrip(']')

    return cls(trad, simp, pinyin)