from enum import Enum


class Weekday(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    @classmethod
    def get_abbreviations(cls):
        return {
            cls.MONDAY: "mon",
            cls.TUESDAY: "tues",
            cls.WEDNESDAY: "wed",
            cls.THURSDAY: "thurs",
            cls.FRIDAY: "fri",
            cls.SATURDAY: "sat",
            cls.SUNDAY: "sun",
        }

    @staticmethod
    def from_short_name(name: str) -> "Weekday":
        for member, abbreviation in Weekday.get_abbreviations().items():
            if abbreviation == name.lower():
                return member
        raise ValueError(f"No enum member found with abbreviation '{name}'")

    @staticmethod
    def from_name(name: str) -> "Weekday":
        for member in Weekday:
            if member.name.lower() == name.lower():
                return member
        raise ValueError(f"No enum member found with name '{name}'")

    def to_short_name(self) -> str:
        return self.get_abbreviations().get(self)

    def add_days(self, days: int) -> "Weekday":
        return Weekday((self.value + days) % 7)
