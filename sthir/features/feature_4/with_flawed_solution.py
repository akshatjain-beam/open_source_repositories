```
    padding_length = int(base2p15[0], 16)
    bit_string = ""
    offset = 0xa1

    for char in base2p15[1:]:
        bit_string += bin(ord(char) - offset)[2:].zfill(15)

    # Remove padding bits from the last 15-bit sequence
    bit_string = bit_string[:-padding_length]
    return bit_string
```