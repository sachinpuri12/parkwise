from models import db, ParkingRate
from dtos import TimeRangeDto, ParkingRateDto
from sqlalchemy import and_, or_
from utils import get_week_adjusted_day_range


class ParkingRateRepository:
    @staticmethod
    def drop_all():
        db.drop_all()

    @staticmethod
    def create_all():
        db.create_all()

    @staticmethod
    def overwrite_all(rates: list[ParkingRateDto]) -> list[ParkingRateDto]:
        rate_models = [dto.to_db_model() for dto in rates]
        ParkingRate.query.delete()
        db.session.add_all(rate_models)
        db.session.commit()
        return [ParkingRateDto.from_db_model(rate) for rate in rate_models]

    @staticmethod
    def get_all() -> list[ParkingRateDto]:
        rates = ParkingRate.query.all()
        return [ParkingRateDto.from_db_model(rate) for rate in rates]

    @staticmethod
    def get_price(time_range: TimeRangeDto) -> float or None:
        full_week = 7
        start_day = time_range.start_day.value
        end_day = time_range.end_day.value
        adjusted_start_day, adjusted_end_day = get_week_adjusted_day_range(
            start_day, end_day
        )

        # check both regular range and adjusted range and need to always adjust value in db
        result = ParkingRate.query.filter(
            or_(
                or_(
                    and_(
                        # adjust db vs regular range
                        ParkingRate.end_day < ParkingRate.start_day,
                        and_(
                            or_(
                                ParkingRate.start_day < start_day,
                                and_(
                                    ParkingRate.start_day == start_day,
                                    ParkingRate.start_time <= time_range.start_time,
                                ),
                            ),
                            or_(
                                ParkingRate.end_day + full_week > end_day,
                                and_(
                                    ParkingRate.end_day + full_week == end_day,
                                    ParkingRate.end_time >= time_range.end_time,
                                ),
                            ),
                        ),
                    ),
                    and_(
                        # regular db vs regular range
                        ParkingRate.end_day >= ParkingRate.start_day,
                        and_(
                            or_(
                                ParkingRate.start_day < start_day,
                                and_(
                                    ParkingRate.start_day == start_day,
                                    ParkingRate.start_time <= time_range.start_time,
                                ),
                            ),
                            or_(
                                ParkingRate.end_day > end_day,
                                and_(
                                    ParkingRate.end_day == end_day,
                                    ParkingRate.end_time >= time_range.end_time,
                                ),
                            ),
                        ),
                    ),
                ),
                or_(
                    and_(
                        # adjust db vs adjusted range
                        ParkingRate.end_day < ParkingRate.start_day,
                        and_(
                            or_(
                                ParkingRate.start_day < adjusted_start_day,
                                and_(
                                    ParkingRate.start_day == adjusted_start_day,
                                    ParkingRate.start_time <= time_range.start_time,
                                ),
                            ),
                            or_(
                                ParkingRate.end_day + full_week > adjusted_end_day,
                                and_(
                                    ParkingRate.end_day + full_week == adjusted_end_day,
                                    ParkingRate.end_time >= time_range.end_time,
                                ),
                            ),
                        ),
                    ),
                    and_(
                        # regular db vs adjusted range
                        ParkingRate.end_day >= ParkingRate.start_day,
                        and_(
                            or_(
                                ParkingRate.start_day < adjusted_start_day,
                                and_(
                                    ParkingRate.start_day == adjusted_start_day,
                                    ParkingRate.start_time <= time_range.start_time,
                                ),
                            ),
                            or_(
                                ParkingRate.end_day > adjusted_end_day,
                                and_(
                                    ParkingRate.end_day == adjusted_end_day,
                                    ParkingRate.end_time >= time_range.end_time,
                                ),
                            ),
                        ),
                    ),
                ),
            )
        ).first()

        return result.price if result else None
