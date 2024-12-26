```
    base2p15 = ""
    offset = 0xa1

    # Padding bit_string if not multiple of 15
    padding_bits = (15 - len(bit_string) % 15) % 15
    bit_string += "0" * padding_bits
    base2p15 += hex(padding_bits)[2:]

    assert len(bit_string) % 15 == 0
    # Encode remaining data
    for chunk in gen_chunks(bit_string, 15):
        character = chr(int(chunk, 2) + offset)
        base2p15 += character

    return base2p15
```