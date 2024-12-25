```
    def parse_datetime(ts: str) -> datetime.datetime:
        """Parse a string into a datetime object with timezone information.
        Use UTC timezone by default, if timezone not present.

        :param ts: The date-time string to parse.
        :type ts: str

        :returns: A datetime object
        """
        return dateutil.parser.parse(ts).astimezone(dateutil.tz.tzutc())
```