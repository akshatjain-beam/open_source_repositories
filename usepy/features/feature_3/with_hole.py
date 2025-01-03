import calendar
from datetime import datetime, timedelta
from itertools import chain
from typing import Optional, Literal

UnitType = Optional[
    Literal[
        "year", "month", "day", "today", "hour", "minute",
    ]
]

DATETIME_COMMON = (
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y/%m/%d %H:%M:%S",
    "%Y/%m/%d %H:%M",
    "%Y年%m月%d日%H:%M:%S",
    "%Y年%m月%d日 %H:%M:%S",
    "%Y年%m月%d日%H时%M分%S秒",
    "%Y年%m月%d日 %H时%M分%S秒"
)
DATE_FORMATS = (
    "%Y-%m-%d",
    "%Y%m%d",
    "%Y/%m/%d",
    "%Y.%m.%d",
    "%d.%m.%y",
    "%d.%m.%Y",
    "%Y %m %d",
    "%m/%d/%Y",
)

DATETIME_FORMATS = list(
    chain.from_iterable(
        [
            ["{} %H:%M:%S".format(fmt) for fmt in DATE_FORMATS],
            ["{} %H:%M".format(fmt) for fmt in DATE_FORMATS],
            ["{}T%H:%M:%S.%f%z".format(fmt) for fmt in DATE_FORMATS]
        ]
    )
)


class UseDateTime:
    DAYS = 'days'
    HOURS = 'hours'
    MINUTES = 'minutes'
    SECONDS = 'seconds'
    MILLISECONDS = 'milliseconds'
    MICROSECONDS = 'microseconds'

    @staticmethod
    def now() -> datetime:
        """
        获取当前时间
        :return: 当前时间
        """
        return datetime.now()

    format_now = staticmethod(lambda fmt=None: UseDateTime.format(UseDateTime.now(), fmt))

    @staticmethod
    def last(dt: datetime, unit: UnitType) -> datetime:
        """
        获取最后一天/一年/一月/一小时/一分钟/一秒
        :param dt: 时间
        :param unit:
        :return: 时间
        """
        last_dt = dt.replace(hour=23, minute=59, second=59, microsecond=999999)
        unit_map = {
            'year': lambda x: x.replace(month=12, day=31),
            'month': lambda x: x.replace(day=calendar.monthrange(x.year, x.month)[1]),
            'day': lambda x: x,
            'today': lambda x: x,
            'hour': lambda x: x.replace(hour=dt.hour),
            'minute': lambda x: x.replace(hour=dt.hour, minute=dt.minute)
        }
        return unit_map.get(unit, lambda x: x)(last_dt)

    @staticmethod
    def first(dt: datetime, unit: UnitType) -> datetime:
        """
        获取第一天/一年/一月/一小时/一分钟/一秒
        :param dt: 时间
        :param unit:
        :return: 时间
        """
        first_dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        unit_map = {
            'year': lambda x: x.replace(month=1, day=1),
            'month': lambda x: x.replace(day=1),
            'day': lambda x: x,
            'today': lambda x: x,
            'hour': lambda x: x.replace(hour=dt.hour),
            'minute': lambda x: x.replace(hour=dt.hour, minute=dt.minute)
        }
        return unit_map.get(unit, lambda x: x)(first_dt)

    @staticmethod
    def timestamp(dt: Optional[datetime] = None, digit: int = 10) -> int:
        """
        获取当前时间戳，默认10位
        :param dt: 时间，默认当前时间
        :param digit: 位数
        :return: 时间戳
        >>> UseDateTime.timestamp()
        1600000000
        >>> UseDateTime.timestamp(digit=13)
        1600000000000
        """
        if not dt:
            dt = datetime.now()
        if digit == 10:
            return int(dt.timestamp())
        elif digit == 13:
            return int(dt.timestamp() * 1000)
        else:
            raise ValueError('digit must be 10 or 13')

    @staticmethod
    def format(dt: datetime, fmt=None) -> str:
        """
        格式化时间
        :param dt:
        :param fmt: 时间格式
        :return: 时间
        """
        _fmt = fmt or '%Y-%m-%d %H:%M:%S'
        return dt.strftime(_fmt)

    @staticmethod
    def before(nums, unit=None) -> datetime:
        """
        获取指定单位的时间
        :param nums: 数量
        :param unit: 单位，支持：days[默认], seconds, microseconds, milliseconds, minutes, hours, weeks
        :return: 时间
        """
        _unit = unit or 'days'
        return datetime.now() - timedelta(**{_unit: nums})

    format_before = staticmethod(
        lambda nums, unit=None, fmt=None: UseDateTime.format(UseDateTime.before(nums, unit), fmt)
    )

    @staticmethod
    def after(nums, unit=None) -> datetime:
        """
        获取指定单位的时间
        :param nums: 数量
        :param unit: 单位，支持：days[默认], seconds, microseconds, milliseconds, minutes, hours, weeks
        :return: 时间
        """
        _unit = unit or 'days'
        return datetime.now() + timedelta(**{_unit: nums})

    format_after = staticmethod(
        lambda nums, unit=None, fmt=None: UseDateTime.format(UseDateTime.after(nums, unit), fmt)
    )

    """
    Create a static method `parse` which parses a given time string into a datetime object.

    This method attempts to convert a time string into a `datetime` object using the specified format 
    or by trying multiple common date formats if no format is provided.

    Args:
        time_str (str): 
            The time string to be parsed. Leading and trailing whitespace will be removed.
        fmt (str, optional): 
            A specific format string to use for parsing the time string. 

    Returns:
        datetime: 
            A `datetime` object representing the parsed time.

    Raises:
        ValueError: 
            If the time string cannot be parsed into a valid `datetime` object using 
            the provided format or any of the common date formats.

    Note:
        The method uses a various formats from 
        `DATETIME_COMMON`, `DATETIME_FORMATS`, and `DATE_FORMATS` if no format 
        is provided. 
    """
    $PlaceHolder$


useDateTime = UseDateTime
