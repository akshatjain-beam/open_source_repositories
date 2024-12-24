```
  m = re.match(r'(.+?) (.+?) \[(.+?)\] /(.+)/', line.strip())
  defs = m.group(4).split('/')

  actual_defs = []
  clfrs = None
  tw_pinyin = None
  for def_ in defs:
    if def_.startswith('CL:'):
      pieces = def_.split(':', 2)[1].split(',')
      clfrs = [Classifier.parse(piece) for piece in pieces]
    elif def_.startswith('Taiwan pr. '):
      tw_pinyin = def_.split('[')[1].rstrip(']')
    else:
      actual_defs.append(def_)

  return CedictWord(
    m.group(1), m.group(2), m.group(3), tw_pinyin, actual_defs, clfrs)
```