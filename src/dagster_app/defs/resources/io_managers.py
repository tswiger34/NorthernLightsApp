import dagster as dg
from dagster_duckdb_polars import DuckDBPolarsIOManager


@dg.definitions
def io_managers():
    return dg.Definitions(resources={"polars_duckdb": DuckDBPolarsIOManager(database="data/analytics_db.duckdb")})
