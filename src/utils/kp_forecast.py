from datetime import datetime

import polars as pl
from pydantic import BaseModel, ConfigDict, field_validator, model_validator

EXPECTED_TIMES = ["00", "03", "06", "09", "12", "15", "18", "21"]


class KpForecastRecord(BaseModel):
    date: str
    start_hour_utc: str
    end_hour_utc: str
    kp_index: str

    @field_validator("date")
    @classmethod
    def _ensure_date_format(cls, value: str):
        """Validates the date is in the correct format M-D.

        Raises:
            ValueError: If the date is not in the correct format
        """
        try:
            _dt = datetime.strptime(value, "%b-%d")
            return value
        except (ValueError, AssertionError):
            raise ValueError(f"Invalid date format: {value}. Expected format: M-D")

    @model_validator(mode="after")
    def _ensure_time_ranges(self):
        if self.start_hour_utc not in EXPECTED_TIMES or self.end_hour_utc not in EXPECTED_TIMES:
            raise ValueError(f"Invalid time range: {self.start_hour_utc}-{self.end_hour_utc}")

        start_idx = EXPECTED_TIMES.index(self.start_hour_utc)
        if start_idx < len(EXPECTED_TIMES) - 1 and EXPECTED_TIMES[start_idx + 1] != self.end_hour_utc:
            raise ValueError(f"Invalid time range: {self.start_hour_utc}-{self.end_hour_utc}")
        if start_idx == len(EXPECTED_TIMES) - 1 and self.end_hour_utc != "00":
            raise ValueError(f"Invalid time range: {self.start_hour_utc}-{self.end_hour_utc}")

    @classmethod
    def from_forecast(cls, date: str, time_range: str, value: str) -> "KpForecastRecord":
        times = time_range.split("-")

        return cls(date=date, start_hour_utc=times[0], end_hour_utc=times[-1], kp_index=value)


class DayForecast(BaseModel):
    forecast_records: list[KpForecastRecord]

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_validator(mode="after")
    def _ensure_times(self):
        """Validates the dates and times are in the correct format and have valid values.

        Raises:
            ValueError: If any of the expected time periods are missing
            ValueError: If there are duplicate forecast records for the same time period
            ValueError: If the forecast records are not all for the same date
        """
        EXPECTED_TIMES = ["00", "03", "06", "09", "12", "15", "18", "21"]
        times_present = {record.start_hour_utc for record in self.forecast_records}
        for expected_time in EXPECTED_TIMES:
            if expected_time not in times_present:
                raise ValueError(f"Missing forecast record for time starting at {expected_time} UTC")
        if len(self.forecast_records) != len(EXPECTED_TIMES):
            raise ValueError("Duplicate forecast records found for the same time period")
        dates_present = {record.date for record in self.forecast_records}
        if len(dates_present) != 1:
            raise ValueError("All forecast records must be for the same date")


class ThreeDayForecast(BaseModel):
    day_forecasts: list[DayForecast]

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def to_polars(self) -> pl.DataFrame:
        records = []
        for day_forecast in self.day_forecasts:
            for record in day_forecast.forecast_records:
                records.append(
                    {
                        "date": record.date,
                        "start_hour_utc": record.start_hour_utc,
                        "end_hour_utc": record.end_hour_utc,
                        "kp_index": record.kp_index,
                    }
                )
        return pl.DataFrame(records)
