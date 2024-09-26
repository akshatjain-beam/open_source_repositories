```
    @staticmethod
    def parse(time_str: str, fmt=None) -> datetime:
        """
        解析时间
        :param time_str: 时间字符串
        :param fmt: 时间格式
        :return: 时间
        """
        s = time_str.strip()
        if fmt is not None:
            return datetime.strptime(s, fmt)
        for fmt in chain.from_iterable((DATETIME_COMMON,
                                        DATETIME_FORMATS,
                                        DATE_FORMATS)):
            try:
                return datetime.strptime(s, fmt)
            except ValueError:
                continue
        raise ValueError(f"No valid date format found for '{s}'")
```