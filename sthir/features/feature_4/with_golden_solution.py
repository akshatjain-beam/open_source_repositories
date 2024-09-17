```
    bit_string = ""
    offset = 0xa1
    padding = int(base2p15[0], 16)
    for character in base2p15[1:-1]:
        character = ord(character) - offset
        bits = bin(character)[2:].zfill(15)
        bit_string += bits

    character = ord(base2p15[-1]) - offset
    bits = bin(character)[2:].zfill(15)[:15 - padding]
    bit_string += bits
    return bit_string
```