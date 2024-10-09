```
STROKE_REGEX = re.compile(r'''
    ^
    (?P<number_start> [12345]*)
    (?P<initial> [ㅎㅁㄱㅈㄴㄷㅇㅅㅂㄹ]*)
    (?P<medial> [ㅗㅏㅜ\-*ㅓㅣ]*)
    (?P<number_end> [67890]*)
    (?P<final> [ㅎㅇㄹㄱㄷㅂㄴㅅㅈㅁ]*)
    $
    ''', re.VERBOSE)
```