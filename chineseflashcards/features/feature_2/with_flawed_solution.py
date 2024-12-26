```
  trad, simp, rest = re.match(r'(.*?) (.*?) \[(.*?)\] /(.*)/', line).groups()
  if trad == simp:
    simp = None
  pinyin = rest.split(' ')[0]
  defs = []
  clfrs = []

  for part in rest.split('/')[1:]:
    if part.startswith('CL:'):
      clfrs = [Classifier.parse(s.strip()) for s in part[3:].split(',')]
    elif part.startswith('Taiwan pr.'):
      tw_pinyin = part[len('Taiwan pr. ['):-1]
    else:
      defs.append(part)

  return CedictWord(
    trad=trad,
    simp=simp,
    pinyin=pinyin,
    tw_pinyin=tw_pinyin if 'tw_pinyin' in locals() else None,
    defs=defs,
    clfrs=clfrs if clfrs else None,
  )
```