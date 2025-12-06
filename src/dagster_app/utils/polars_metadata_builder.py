from typing import Any, Optional

import dagster as dg
import polars as pl
from pydantic import BaseModel


class PolarsMetadata(BaseModel):
    table_sample: dg.TableMetadataValue
    table_stats: dg.TableMetadataValue
    row_count: dg.IntMetadataValue
    categorical_fields: dg.JsonMetadataValue | None = None


class PolarsMetadataBuilder:
    def __init__(self, df: pl.DataFrame):
        self.df = df

    def _build_categorical_field_values(self, max_unique_values: int = 8) -> dict[str, list[Any]]:
        """Collect categorical values for string columns with limited cardinality."""
        categorical_values: dict[str, list[Any]] = {}
        for column_name, column_type in self.df.schema.items():
            if column_type != pl.Utf8:
                continue
            series = self.df.get_column(column_name)
            non_null_unique_count = series.drop_nulls().n_unique()
            include_null = series.null_count() > 0
            total_unique = non_null_unique_count + (1 if include_null else 0)
            if total_unique > max_unique_values:
                continue
            non_null_unique_values = series.drop_nulls().unique(maintain_order=True)
            values = [self._coerce_value(value) for value in non_null_unique_values.to_list()]
            if include_null:
                values.append(None)
            categorical_values[column_name] = values
        return categorical_values

    @staticmethod
    def _coerce_value(value: Any) -> Any:
        """Ensure values stored in Dagster metadata are JSON-serialisable primitives."""
        if value is None or isinstance(value, (str, int, float, bool)):
            return value
        if hasattr(value, "isoformat"):
            try:
                return value.isoformat()
            except Exception:  # pragma: no cover - defensive
                pass
        return str(value)

    def build_dagster_metadata_table(
        self, data_base_model: Optional[type[BaseModel]] = None
    ) -> dg.TableMetadataValue:
        """Create Dagster TableMetadataValue from a Polars DataFrame.

        Args:
            data_base_model (Optional[BaseModel], optional): If the data frame is based on an existing Pydantic
            model, pass in the **UNINSTANCIATED** base model. This allows for field descriptions and table constraints
            to be materialized in Dagster as well. Defaults to None.

        Returns:
            dg.TableMetadataValue: _description_

        Example:
            ```python
            import dagster as dg
            import polars as pl
            from dagster_app.defs.utils.metadata_helpers import PolarsMetadata
            from .models import MyDataModel


            @dg.asset
            def my_asset(context: dg.AssetExecutionContext):
                ...
                df = pl.DataFrame(...)  # A polars data frame that is based on MyDataModel
                metadata_builder = PolarsMetadataBuilder(df)
                table_metadata = metadata_builder.build_dagster_metadata_table(
                    data_base_model=MyDataModel
                )  # Note: pass in the uninstantiated model class, e.g. MyDataModel, not MyDataModel()
                return dg.MaterializeResult(metadata={"table": table_metadata})
            ```
        """
        raw_samples = self.df.head(5).to_dicts()
        sample_data = [{column: self._coerce_value(value) for column, value in row.items()} for row in raw_samples]
        if data_base_model is None:
            schema = dg.TableSchema.from_name_type_dict(
                {col_name: col_type._string_repr() for col_name, col_type in self.df.schema.items()}
            )
        else:
            schema = dg.TableSchema(
                columns=[
                    dg.TableColumn(
                        name=field_name, type=str(field_info.annotation), description=field_info.description
                    )
                    for field_name, field_info in data_base_model.model_fields.items()
                ]
            )
        return dg.TableMetadataValue(
            records=[dg.TableRecord(sample) for sample in sample_data],
            schema=schema,
        )

    def build_table_stats_metadata(self) -> dg.TableMetadataValue:
        """Generate table statistics metadata from the Polars DataFrame. This will include all table statistics
        from `df.describe()`.

        Returns:
            dg.TableMetadataValue: Metadata containing statistical summary of the DataFrame.

        Example:
            ```python
            import dagster as dg
            import polars as pl
            from dagster_app.defs.utils.metadata_helpers import PolarsMetadata


            @dg.asset
            def my_asset(context: dg.AssetExecutionContext):
                ...
                df = pl.DataFrame(...)  # A polars data frame
                metadata_builder = PolarsMetadataBuilder(df)
                table_stats = metadata_builder.build_table_stats_metadata()
                return dg.MaterializeResult(metadata={"table_stats": table_stats})
            ```
        """
        table_stats = self.df.describe()
        return dg.TableMetadataValue(
            records=[dg.TableRecord(stat) for stat in table_stats.to_dicts()],
            schema=dg.TableSchema.from_name_type_dict(
                {col_name: col_type._string_repr() for col_name, col_type in table_stats.schema.items()}
            ),
        )

    def build_table_level_metadata(self, data_base_model: Optional[type[BaseModel]] = None) -> dict[str, Any]:
        """Build both the table metadata and table statistics metadata.

        Args:
            data_base_model (Optional[type[BaseModel]], optional): If the data frame is based on an existing Pydantic
                model, pass in the **UNINSTANCIATED** base model. This allows for field descriptions and table constraints
                to be materialized in Dagster as well. Defaults to None.

        Returns:
            metadata (dict[str, Any]): A dictionary containing both the table metadata and table statistics metadata.
        """
        tbl_shape = self.df.shape
        metadata: dict[str, Any] = {
            "table_sample": self.build_dagster_metadata_table(data_base_model=data_base_model),
            "table_stats": self.build_table_stats_metadata(),
            "row_count": dg.MetadataValue.int(tbl_shape[0]),
        }
        categorical_values = self._build_categorical_field_values()
        if categorical_values:
            metadata["categorical_fields"] = dg.MetadataValue.json(categorical_values)
        return metadata
