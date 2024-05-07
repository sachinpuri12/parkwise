from marshmallow import Schema, fields, validates, ValidationError, validates_schema
from flask_marshmallow import Marshmallow
from enums import Weekday
from datetime import datetime
from pytz import timezone, UnknownTimeZoneError
from exceptions import InputExceedsAllowedRangeError
from converters import convert_datetime_to_utc

ma = Marshmallow()


class ParkingRateSchema(ma.Schema):
    days = ma.String(required=True)
    times = ma.String(required=True)
    tz = ma.String(required=False)
    price = ma.Float(required=True)

    @validates("days")
    def validate_days(self, value):
        valid_weekdays = Weekday.get_abbreviations().values()
        for day in value.split(","):
            if day.lower().strip() not in valid_weekdays:
                raise ValidationError(
                    f"Invalid day: {day}, must be one of {list(valid_weekdays)}"
                )

    @validates("times")
    def validate_times(self, value):
        try:
            start_time, end_time = [
                datetime.strptime(time, "%H%M").time() for time in value.split("-")
            ]
            if start_time >= end_time:
                raise ValidationError(
                    f"Invalid time range: {value}, start time must be before end time"
                )
        except ValueError:
            raise ValidationError(f"Invalid time range: {value}. Please use HHMM-HHMM")

    @validates("tz")
    def validate_tz(self, value):
        try:
            timezone(value)
        except UnknownTimeZoneError:
            raise ValidationError(f"Invalid timezone: {value}")

    @validates("price")
    def validate_price(self, value):
        if value < 0:
            raise ValidationError(f"Invalid price: {value}, must be greater than 0")


class PutRatesInputSchema(Schema):
    rates = fields.List(fields.Nested(ParkingRateSchema), required=True)


class GetRatesInputSchema(Schema):
    timezone = fields.String(required=False)

    @validates("timezone")
    def validate_tz(self, value):
        try:
            timezone(value)
        except UnknownTimeZoneError:
            raise ValidationError(f"Invalid timezone: {value}")


class GetPriceInputSchema(Schema):
    start = ma.String(required=True)
    end = ma.String(required=True)

    @validates("start")
    def validate_start(self, value):
        try:
            convert_datetime_to_utc(datetime.fromisoformat(value))
        except ValueError:
            raise ValidationError(
                f"Invalid start value: {value}. Please use ISO-8601 format (YYYY-MM-DDTHH:MM:SSZ)"
            )

    @validates("end")
    def validate_end(self, value):
        try:
            convert_datetime_to_utc(datetime.fromisoformat(value))
        except ValueError:
            raise ValidationError(
                f"Invalid end value: {value}. Please use ISO-8601 format (YYYY-MM-DDTHH:MM:SSZ)"
            )

    @validates_schema
    def validate_time_range(self, data, **kwargs):
        start = convert_datetime_to_utc(datetime.fromisoformat(data["start"]))
        end = convert_datetime_to_utc(datetime.fromisoformat(data["end"]))
        if start >= end:
            raise ValidationError(
                f"Invalid time range: {start} to {end}, start time must be before end time"
            )
        if (end - start).days > 0:
            raise InputExceedsAllowedRangeError(
                f"Invalid time range: {start} to {end}, must not exceed one day"
            )
