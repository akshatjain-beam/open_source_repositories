from usepy import useString


def test_get_middle():
    # Test to extract the substring between 'abc' and 'def'
    assert useString.get_middle('abc123def', 'abc', 'def') == '123'
    # Test to extract the substring starting after 'abc' to the end
    assert useString.get_middle('abc123def', 'abc') == '123def'
    # Test to extract the substring from the beginning to 'def'
    assert useString.get_middle('abc123def', end_str='def') == 'abc123'


def test_get_middle_batch():
    # Test to extract multiple substrings between 'abc' and 'def'
    assert useString.get_middle_batch('abc123def456abc789def', 'abc', 'def') == ['123', '789']
    # Test to limit the extraction to the first substring only
    assert useString.get_middle_batch('abc123def456abc789def', 'abc', 'def', 1) == ['123']
    # Test to extract substrings using only the end delimiter
    assert useString.get_middle_batch('abc123def456abc789def', end_str="def") == ['abc123', '456abc789']
    # Test to extract from the start delimiter to the end of the string
    assert useString.get_middle_batch('abc123def456abc789def', start_str="abc") == ['123def456abc789def']


def test_get_left():
    # Test to get the substring to the left of 'def'
    assert useString.get_left('abc123def', 'def') == 'abc123'
    # Test to get the substring to the left of 'abc'
    assert useString.get_left('abc123def', 'abc') == ''
    # Test to get the substring to the left of '123'
    assert useString.get_left('abc123def', '123') == 'abc'


def test_get_right():
    # Test to get the substring to the right of 'abc'
    assert useString.get_right('abc123def', 'abc') == '123def'
    # Test to get the substring to the right of 'def'
    assert useString.get_right('abc123def', 'def') == ''
    # Test to get the substring to the right of '123'
    assert useString.get_right('abc123def', '123') == 'def'


def test_reverse():
    # Test to reverse an empty string
    assert useString.reverse('') == ''
    # Test to reverse a simple string
    assert useString.reverse('abc') == 'cba'
    # Test to reverse a string with numbers
    assert useString.reverse('abc123') == '321cba'
    # Test to reverse a longer string
    assert useString.reverse('abc123def') == 'fed321cba'


def test_uuid():
    # Test to ensure that two UUIDs generated are different
    assert useString.uuid() != useString.uuid()
    # Test to check the length of the generated UUID
    assert len(useString.uuid()) == 32


def test_to_str():
    # Test to convert an integer to a string
    assert useString.to_str(1) == '1'
    # Test to convert a float to a string
    assert useString.to_str(1.1) == '1.1'
    # Test to convert a boolean to a string
    assert useString.to_str(True) == 'True'
    # Test to convert None to a string
    assert useString.to_str(None) == 'None'
    # Test to convert a list to a string
    assert useString.to_str([1, 2, 3]) == '[1, 2, 3]'
    # Test to convert a dictionary to a string
    assert useString.to_str({'a': 1, 'b': 2}) == "{'a': 1, 'b': 2}"
    # Test to convert a bytes object to a string
    assert useString.to_str(b'miclon') == "miclon"


def test_to_bytes():
    # Test to convert a string to bytes using the default encoding
    assert useString.to_bytes('miclon') == b'miclon'
    # Test to convert a string to bytes specifying UTF-8 encoding
    assert useString.to_bytes('miclon', encoding='utf-8') == b'miclon'
    # Test to convert a string with non-ASCII characters to bytes using UTF-8
    assert useString.to_bytes('米乐', encoding='utf-8') == b'\xe7\xb1\xb3\xe4\xb9\x90'
    # Test to convert a string with non-ASCII characters to bytes using GBK encoding
    assert useString.to_bytes('米乐', encoding='gbk') == b'\xc3\xd7\xc0\xd6'
    # Test to convert bytes back to a string using GBK encoding
    assert useString.to_str(useString.to_bytes('米乐', encoding='gbk'), encoding='gbk') == '米乐'


def test_random():
    # Test to ensure two random strings of the same length are different
    assert useString.random(10) != useString.random(10)
    # Test to ensure a random string of fixed length is correct
    assert len(useString.random(min_len=10, max_len=10)) == 10
    # Test to ensure a random string does not exceed the maximum length
    assert len(useString.random(max_len=3)) <= 3
    # Test to ensure a random string meets the minimum length requirement
    assert len(useString.random(min_len=30)) >= 30
