    match = re.match(r'^(.+?) (.+?) \[(.+?)\] /(.*)/$', line)
    if not match:
      raise ValueError('line does not match expected format: {}'.format(repr(line)))

    trad, simp, pinyin, defs_str = match.groups()

    defs = []
    clfrs = []
    tw_pinyin = None

    for piece in defs_str.split('/'):
      if piece.startswith('CL:'):
        for clfr_str in piece[len('CL:'):].split(','):
          clfrs.append(Classifier.parse(clfr_str.strip()))
      elif piece.startswith('Taiwan pr.'):
        tw_pinyin = piece[len('Taiwan pr. '):][1:-1]
      else:
        defs.append(piece.strip())

    return CedictWord(trad, simp, pinyin, tw_pinyin, defs, clfrs or None)