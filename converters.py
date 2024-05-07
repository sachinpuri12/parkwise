from datetime import datetime, timedelta
from enums import Weekday
from dtos import ParkingRateDto, TimeRangeDto
from utils import (
    get_utc_offset_minutes,
    convert_datetime_to_utc,
    should_increment_days,
    should_decrement_days,
    add_minutes_to_time,
)
import pdb


def parse_rates(data: dict) -> list[ParkingRateDto]:
    rate_dtos = []
    rates = data["rates"]
    for rate in rates:
        price = float(rate.get("price"))
        timezone = rate.get("tz", "UTC")
        start_time, end_time = [
            datetime.strptime(time, "%H%M").time()
            for time in rate.get("times").split("-")
        ]
        days = [
            Weekday.from_short_name(day.lower().strip())
            for day in rate.get("days").split(",")
        ]
        dtos = [
            ParkingRateDto(
                start_day=day,
                start_time=start_time,
                end_day=day,
                end_time=end_time,
                price=price,
            )
            for day in days
        ]
        adjusted_dtos = adjust_rates_for_timezone(dtos, timezone, True)
        rate_dtos.extend(adjusted_dtos)
    return rate_dtos


def get_unique_timezones(data: dict) -> list[str]:
    return list(set([rate.get("tz", "UTC") for rate in data["rates"]]))


def adjust_rates_for_timezone(
    rate_dtos: list[ParkingRateDto], timezone: str, to_utc: bool
) -> list[ParkingRateDto]:
    delta_minutes = timedelta(minutes=(get_utc_offset_minutes(timezone)))
    if to_utc:
        delta_minutes *= -1
    adjusted_dtos = []

    for rate in rate_dtos:
        delta_end_days, delta_start_days = 0, 0
        if should_increment_days(rate.start_time, delta_minutes):
            delta_start_days = 1
        if should_increment_days(rate.end_time, delta_minutes):
            delta_end_days = 1
        if should_decrement_days(rate.start_time, delta_minutes):
            delta_start_days = -1
        if should_decrement_days(rate.end_time, delta_minutes):
            delta_end_days = -1

        adjusted_start_day = rate.start_day.add_days(delta_start_days)
        adjusted_end_day = rate.end_day.add_days(delta_end_days)
        adjusted_start_time = add_minutes_to_time(rate.start_time, delta_minutes)
        adjusted_end_time = add_minutes_to_time(rate.end_time, delta_minutes)
        adjusted_dtos.append(
            ParkingRateDto(
                start_day=adjusted_start_day,
                start_time=adjusted_start_time,
                end_day=adjusted_end_day,
                end_time=adjusted_end_time,
                price=rate.price,
            )
        )
    return adjusted_dtos


def consolidate_rates(rate_dtos: list[ParkingRateDto], timezone="UTC") -> list[dict]:
    consolidated_rates = []
    adjusted_dtos = adjust_rates_for_timezone(rate_dtos, timezone, False)
    for rate in adjusted_dtos:
        consolidated_rates.append(
            {
                "start": f"{rate.start_day.name} {rate.start_time.strftime('%H:%M')}",
                "end": f"{rate.end_day.name} {rate.end_time.strftime('%H:%M')}",
                "price": rate.price,
                "timezone": timezone,
            }
        )
    return consolidated_rates


def parse_time_range(data: dict) -> TimeRangeDto:
    start = convert_datetime_to_utc(datetime.fromisoformat(data["start"]))
    end = convert_datetime_to_utc(datetime.fromisoformat(data["end"]))
    start_day = Weekday.from_name(start.strftime("%A").lower())
    end_day = Weekday.from_name(end.strftime("%A").lower())
    return TimeRangeDto(
        start_day=start_day,
        start_time=start.time(),
        end_day=end_day,
        end_time=end.time(),
    )
