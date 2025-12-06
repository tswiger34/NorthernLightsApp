from typing import Any

import dagster as dg

from dagster_app.utils.metadata import MetadataBaseClass


class KpForecastDefinitionMetadata(MetadataBaseClass):
    source_url: dg.UrlMetadataValue = dg.UrlMetadataValue("https://services.swpc.noaa.gov/text/3-day-forecast.txt")


class KpForecastRunMetadata(MetadataBaseClass):
    retrieval_time: str
    forecast_dates: list[str]
    row_count: int
    table_output: dg.TableMetadataValue

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_url": self.source_url,
            "retrieval_time": self.retrieval_time,
            "forecast_dates": self.forecast_dates,
            "row_count": self.row_count,
            "table_output": self.table_output,
        }
