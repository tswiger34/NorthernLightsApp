import dagster as dg
import polars as pl

from dagster_app.defs.resources.httpx_client import WebClient
from dagster_app.utils.polars_metadata_builder import PolarsMetadataBuilder
from utils.kp_forecast import DayForecast, ThreeDayForecast

from .models import KpForecastDefinitionMetadata, KpForecastRunMetadata  # noqa


@dg.asset(
    kinds=["Python"],
    name="three_day_kp_forecast",
    key_prefix="raw",
    group_name="noaa_data",
    metadata=KpForecastDefinitionMetadata().to_dg_metadata(),
    io_manager_key="polars_duckdb",
    description="The 3-hour forecast of the Kp index from NOAA, updated every 3 hours and covers the next 3 days",
)
def three_day_kp_forecast(context: dg.AssetExecutionContext, noaa_client: WebClient) -> pl.DataFrame:
    response = noaa_client.client.get("https://services.swpc.noaa.gov/text/3-day-forecast.txt")
    response.raise_for_status()
    forecast = response.text
    lines = forecast.splitlines()
    forecast_table_start = next(i for i, line in enumerate(lines) if "NOAA Kp index breakdown" in line)
    data_lines = lines[forecast_table_start + 2 : forecast_table_start + 11]
    date_parts = lines[forecast_table_start + 2].strip().split()
    dates = []
    for i in range(0, 5, 2):
        month = date_parts[i]
        day = date_parts[i + 1]
        full_date = f"{month}-{day}"
        dates.append(full_date)
    time_periods = []
    values = []
    for line in data_lines[1:]:
        if not line.strip():
            continue
        parts = line.split()
        for i in parts:
            if "(" in i:
                parts.remove(i)
        time_periods.append(parts[0])
        values.append(parts[1:])
    values = values
    time_periods = time_periods

    df = ThreeDayForecast(
        day_1=DayForecast.from_forecast(dates, values, 0),
        day_2=DayForecast.from_forecast(dates, values, 1),
        day_3=DayForecast.from_forecast(dates, values, 2),
    ).to_dataframe()
    context.log.info("Successfully fetched and parsed 3-day KP forecast")
    print(df)
    return dg.MaterializeResult(metadata=PolarsMetadataBuilder(df=df).build_table_level_metadata(), value=df)
