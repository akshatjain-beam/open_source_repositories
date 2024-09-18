```
def process_documents(documents):
    base2p15_arrs = list()
    for document in documents:
        bit_arr = bitarray()
        with open(document[0], "rb") as f:
            bit_arr.fromfile(f)
        base2p15 = base2p15_encode(bit_arr.to01())
        document = [base2p15] + document[1:]
        base2p15_arrs.append(document)
    return base2p15_arrs
```