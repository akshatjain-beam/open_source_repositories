```
def process_documents(documents: list) -> list:
    """
    Processes a list of documents by encoding their binary content and preserving metadata.

    Implementation Details:
    1. Iterate over the documents and do the following:
    2. Initialize an empty bitarray instance.
    3. Open the binary file and convert its content into a binary string.
    4. Encode the binary string using the base2p15_encode function.
    5. Create a list containing the encoded data and document metadata from index 1 to
    the end of the list.
    6. Add the data from index 0, to the end of list.
    7. Append this list to the base2p15_arrs list.

    Args:
    documents (list): A list of documents where each document is represented as a list
    of elements
    Returns:
    base2p15_arrs (list): A list of lists
    """
    base2p15_arrs = list()
    for document in documents:
        bit_array = bitarray()
        with open(document[0], "rb") as f:
            bit_array.frombytes(f.read())
        encoded = base2p15_encode(bit_array.to01())
        temp = document[1:]
        temp.insert(0, encoded)
        base2p15_arrs.append(temp)
    return base2p15_arrs
```