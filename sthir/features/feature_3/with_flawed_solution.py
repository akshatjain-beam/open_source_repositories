```
    padding_len = 15 - (len(bit_string) % 15) if len(bit_string) % 15 != 0 else 0
    bit_string = bit_string + '0' * padding_len
    encoded_string = hex(padding_len)[2:]
    for chunk in gen_chunks(bit_string, 15):
        number = int(chunk, 2)
        encoded_string += chr(number + 0xa1)
    return encoded_string

```