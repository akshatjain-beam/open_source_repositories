@staticmethod
def get_middle_batch(
        original_str: str,
        start_str: Optional[str] = None,
        end_str: Optional[str] = None,
        limit: Optional[int] = None
) -> list[str]:
    """
    获取字符串中间内容，批量获取
    :param original_str: 原始字符串
    :param start_str: 开始字符串
    :param end_str: 结束字符串
    :param limit: 限制数量
    :return: 中间内容列表
    >>> UseString.get_middle_batch('abc123defabc456def', 'abc', 'def')
    ['123', '456']
    """
    find_str_list = []
    original_str_temp = original_str
    while True:
        find_str, start, end = UseString._get_section(original_str_temp, start_str, end_str)
        if find_str is None:
            break
        find_str_list.append(find_str)
        original_str_temp = original_str_temp[end:]
        if limit and len(find_str_list) >= limit:
            break
    return find_str_list