```
    if len(base2p15) <= 1:
        return ''
    padding_bits = int(base2p15[0], 16)
    bit_string = ''
    for char in base2p15[1:-1]:
        # Convert the character to its Unicode code point
        code_point = ord(char)
        
        # Subtract the offset to get the 15-bit value
        value = code_point 
        
        # Convert the 15-bit value to a binary string of length 15 (padded with leading zeros)
        bit_string += format(value, '015b')
    
    # Handle the last character separately to remove padding
    last_char = base2p15[-1]
    code_point = ord(last_char)
    value = code_point 
    bit_string += format(value, '015b')[:15 - padding_bits]
    return bit_string
```