from pydantic import BaseModel, Field  # noqa
import dagster as dg
from datetime import datetime
from typing import Any


class MetadataBaseClass(BaseModel):
    def _to_metadata_value(self, value: Any) -> dg.MetadataValue:
        if isinstance(value, (dg.MetadataValue, dg.TableMetadataValue, dg.IntMetadataValue)):
            return value
        if isinstance(value, bool):
            return dg.MetadataValue.bool(value)
        if isinstance(value, int):
            return dg.MetadataValue.int(value)
        if isinstance(value, float):
            return dg.MetadataValue.float(value)
        if isinstance(value, datetime):
            return dg.MetadataValue.timestamp(value)
        if isinstance(value, dict):
            return dg.MetadataValue.json(value)
        if isinstance(value, str):
            stripped = value.strip()
            if stripped.isdigit() or (stripped.startswith("-") and stripped[1:].isdigit()):
                return dg.MetadataValue.int(int(stripped))
            try:
                float_val = float(stripped)
                return dg.MetadataValue.float(float_val)
            except ValueError:
                pass
            lowered = stripped.lower()
            if lowered in {"true", "false"}:
                return dg.MetadataValue.bool(lowered == "true")
            return dg.MetadataValue.text(value)
        return dg.MetadataValue.text(str(value))

    def _clean_key_name(self, key: str | None):
        key_info = self.__class__.model_fields[key]
        return key_info.alias or key

    def to_dg_metadata(self, additional_metadata: dict[str, dg.MetadataValue] | None = None) -> dict[str, Any]:
        """Turns a Metadata model into a dictionary of dagster metadata values, along with any an option to add
        additional metadata that is already in a dictionary of dagster metadata values

        Args:
            additional_metadata (dict[str, dg.MetadataValue]): The additional metadata values that are already
              formatted as a dictionary of dagster metadata values

        Returns:
            dict[str, Any]: A dictionary of dagster metadata values ready to be materialized
        """
        metadata = {
            self._clean_key_name(metadata_key): self._to_metadata_value(value=metadata_value)
            for metadata_key, metadata_value in self.__dict__.items()
        }
        if not additional_metadata:
            return metadata
        metadata.update(**additional_metadata)
        return metadata
