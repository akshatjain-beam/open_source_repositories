```
    bit_string = ""
    offset = 0xa1
    padding_bits = int(base2p15[0], 16)
    for character in base2p15[1:]:
        bit_string += f'{ord(character) - offset:015b}'
    return bit_string[:-padding_bits]
```