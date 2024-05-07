from enums import Weekday
from models import ParkingRate
from datetime import datetime


class ParkingRateDto:
    def __init__(
        self,
        start_day: Weekday,
        start_time: datetime,
        end_day: Weekday,
        end_time: datetime,
        price: float,
    ):
        self.start_day = start_day
        self.start_time = start_time
        self.end_day = end_day
        self.end_time = end_time
        self.price = price

    @classmethod
    def from_dict(cls, data: dict) -> "ParkingRateDto":
        return cls(
            start_day=Weekday.from_short_name(data["start_day"]),
            start_time=data["start_time"],
            end_day=Weekday.from_short_name(data["end_day"]),
            end_time=data["end_time"],
            price=float(data["price"]),
        )

    def to_dict(self) -> dict:
        return {
            "start_day": self.start_day.to_short_name(),
            "start_time": self.start_time.strftime("%H%M"),
            "end_day": self.end_day.to_short_name(),
            "end_time": self.end_time.strftime("%H%M"),
            "price": self.price,
        }

    def to_db_model(self) -> ParkingRate:
        return ParkingRate(
            start_day=self.start_day.value,
            start_time=self.start_time,
            end_day=self.end_day.value,
            end_time=self.end_time,
            price=self.price,
        )

    @staticmethod
    def from_db_model(rate: ParkingRate) -> "ParkingRateDto":
        return ParkingRateDto(
            start_day=Weekday(int(rate.start_day)),
            start_time=rate.start_time,
            end_day=Weekday(int(rate.end_day)),
            end_time=rate.end_time,
            price=rate.price,
        )


class TimeRangeDto:
    def __init__(
        self,
        start_day: Weekday,
        start_time: datetime,
        end_day: Weekday,
        end_time: datetime,
    ):
        self.start_day = start_day
        self.start_time = start_time
        self.end_day = end_day
        self.end_time = end_time
