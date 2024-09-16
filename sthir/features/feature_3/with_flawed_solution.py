```
    padding_length = 15 - len(bit_string) % 15
    bit_string = bit_string + '0' * padding_length
    encoded_string = hex(padding_length)[2:]
    for chunk in gen_chunks(bit_string, 15):
        integer_representation = int(chunk, 2)
        encoded_string += chr(integer_representation + 0xa1)
    return encoded_string
```