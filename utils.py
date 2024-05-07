from datetime import datetime, timedelta
from pytz import timezone, UTC


def get_utc_offset_minutes(tz_str: str) -> int:
    return int(datetime.now(timezone(tz_str)).utcoffset().total_seconds() / 60)


def convert_datetime_to_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def should_increment_days(time: datetime, delta_minutes: int) -> bool:
    date_with_time = datetime.combine(datetime.today(), time)
    if (date_with_time + delta_minutes).date() > date_with_time.date():
        return True
    return False


def should_decrement_days(time: datetime, delta_minutes: timedelta) -> bool:
    date_with_time = datetime.combine(datetime.today(), time)
    if (date_with_time + delta_minutes).date() < date_with_time.date():
        return True
    return False


def add_minutes_to_time(time: datetime, delta_minutes: timedelta) -> datetime:
    date_with_time = datetime.combine(datetime.today(), time)
    return (date_with_time + delta_minutes).time()


def add_days(start: int, delta: int) -> int:
    return (start + delta) % 7


def get_week_adjusted_day_range(start_day: int, end_day: int) -> tuple[int, int]:
    if end_day < start_day:
        return start_day, end_day + 7
    return start_day + 7, end_day + 7
