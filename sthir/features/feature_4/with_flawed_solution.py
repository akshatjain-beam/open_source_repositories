```
    bit_string = ""
    offset = 0xa1
    padding_bits = int(base2p15[0], 16)
    base2p15 = base2p15[1:]
    for character in base2p15:
        bit_string += bin(ord(character) - offset)[2:].zfill(15)
    return bit_string[:-padding_bits]
```