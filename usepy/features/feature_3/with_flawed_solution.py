```
    @staticmethod
    def parse(time_str: str, fmt: Optional[str] = None) -> datetime:
        time_str = time_str.strip()
        if fmt:
            return datetime.strptime(time_str, fmt)
        try:
            return datetime.strptime(time_str, fmt)
        except ValueError:
            for fmt in DATETIME_COMMON + DATETIME_FORMATS + DATE_FORMATS:
                try:
                    return datetime.strptime(time_str, fmt)
                except ValueError:
                    pass
            raise ValueError(f"Time string '{time_str}' does not match any known format.")
```