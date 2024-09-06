@staticmethod
def get_middle_batch(
        original_str: str,
        start_str: Optional[str] = None,
        end_str: Optional[str] = None,
        max_count: Optional[int] = None
) -> list:
    """
    获取字符串中间内容
    :param original_str: 原始字符串
    :param start_str: 开始字符串
    :param end_str: 结束字符串
    :param max_count: 最大数量
    :return: 中间内容
    >>> UseString.get_middle_batch('abc123def456abc789def', 'abc', 'def')
    ['123', '789']
    >>> UseString.get_middle_batch('abc123def456abc789def', 'abc', 'def', 1)
    ['123']
    """
    result = []
    while True:
        find_str, start_, end_ = UseString._get_section(original_str, start_str, end_str)
        if find_str is None:
            break
        result.append(find_str)
        original_str = original_str[end_ + len(end_str or ''):]
    return result[:max_count]