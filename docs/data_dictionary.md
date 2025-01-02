# Data Dictionary

## Overview
This document provides detailed information about the datasets used in the project. Each variable is described with its name, type, description, and any additional notes or constraints. The datasets include the Solar Weather dataset, Earth Weather dataset, Location dataset, Light Pollution dataset, and General dataset.

---

## Table of Contents
1. [Solar Weather Dataset](#solar-weather-dataset)
    1. [Dataset Summary](#dataset-summary)
    2. [Variable Details](#variable-details)
2. [Earth Weather Dataset](#earth-weather-dataset)
    1. [Dataset Summary](#dataset-summary-1)
    2. [Variable Details](#variable-details-1)
3. [Locations Dataset](locations-dataset)
    1. [Dataset Summary](#dataset-summary-2)
    2. [Variable Details](#variable-details-2)
4. [Light Pollution Dataset](#light-pollution-dataset)
    1. [Dataset Summary](#dataset-summary-3)
    2. [Variable Details](#variable-details-3)
5. [General Dataset](#general-dataset)
    1. [Dataset Summary](#dataset-summary-4)
    2. [Variable Details](#variable-details-4)
6. [Notes and References](#notes-and-references)
7. [Change Log](#changelog)

---

## Solar Weather Dataset

### Dataset Summary
- **Dataset Name**: `Solar Weather`
- **Description**: This dataset is where all historical observations and predictions will be stored for solar weather. This will include important features for forcasting the Northern Lights such as Kp index, radio flux, sun spots, etc. There will be seperate tables for different periodicities, inlcuding minute, hour, and daily time scales as different variables are measured at different time scales.
- **Source**: All of this data was sourced from NOAA's public data sources. A link to the exact data source associated with each variable can be found in the [Notes and References](#notes-and-references) section.
- **Tables**: TBD
- **Number of Variables**: TBD
- **Number of Records**: TBD
- **Last Updated**: `2025-01-02`

---

### Variable Details

| Variable Name | Data Type  | Description                         | Allowed Values/Range     | Notes                          |
|---------------|------------|-------------------------------------|--------------------------|--------------------------------|
| `[TableName]WeatherID`  | `INT`   | This is the unqiue identifier for each record  | 0-2,147,483,647 | This will be autoincremented starting at 0 | N/A |
| `DateID`  | `INT`  | This identifies the date of the record and is associated with a date value in the date table  | 0-2,147,483,647 | This will save space over using strings for dates |
| `SolarWindSpeed`  | `REAL`  | This is a measurement of the solar wind speed in | Unsure | **Add Units** |

---

## Earth Weather Dataset

### Dataset Summary
- **Dataset Name**: `Earth Weather`
- **Description**:
- **Source**: All of this data was sourced from **TBD**. A link to the exact data source associated with each variable can be found in the [Notes and References](#notes-and-references) section.
- **Tables**: TBD
- **Number of Variables**: TBD
- **Number of Records**: TBD
- **Last Updated**: `2025-01-02`

---

### Variable Details

| Variable Name | Data Type  | Description                         | Allowed Values/Range     | Notes                          |
|---------------|------------|-------------------------------------|--------------------------|--------------------------------|
| `[TableName]WeatherID`  | `INT`   | This is the unqiue identifier for each record  | 0-2,147,483,647 | This will be autoincremented starting at 0 | N/A |
| `DateID`  | `INT`  | This identifies the date of the record and is associated with a date value in the date table  | 0-2,147,483,647 | This will save space over using strings for dates |
| `SolarWindSpeed`  | `REAL`  | This is a measurement of the solar wind speed in | Unsure | **Add Units** |
---

## Locations Dataset

### Dataset Summary
- **Dataset Name**: `Locations`
- **Description**:
- **Source**: All of this data was sourced from **TBD**. A link to the exact data source associated with each variable can be found in the [Notes and References](#notes-and-references) section.
- **Tables**: TBD
- **Number of Variables**: TBD
- **Number of Records**: TBD
- **Last Updated**: `2025-01-02`

---

### Variable Details

| Variable Name | Data Type  | Description                         | Allowed Values/Range     | Notes                          |
|---------------|------------|-------------------------------------|--------------------------|--------------------------------|
| `LocationID`  | `INT`   | This is the unqiue identifier for each record  | 0-2,147,483,647 | This will be autoincremented starting at 0 | N/A |
| `DateID`  | `INT`  | This identifies the date of the record and is associated with a date value in the date table  | 0-2,147,483,647 | This will save space over using strings for dates |
| `SolarWindSpeed`  | `REAL`  | This is a measurement of the solar wind speed in | Unsure | **Add Units** |
---

## Light Pollution Dataset

### Dataset Summary
- **Dataset Name**: `Light Pollution`
- **Description**:
- **Source**: All of this data was sourced from **TBD**. A link to the exact data source associated with each variable can be found in the [Notes and References](#notes-and-references) section.
- **Tables**: TBD
- **Number of Variables**: TBD
- **Number of Records**: TBD
- **Last Updated**: `2025-01-02`

---

### Variable Details

| Variable Name | Data Type  | Description                         | Allowed Values/Range     | Notes                          |
|---------------|------------|-------------------------------------|--------------------------|--------------------------------|
| `[TableName]WeatherID`  | `INT`   | This is the unqiue identifier for each record  | 0-2,147,483,647 | This will be autoincremented starting at 0 | N/A |
| `DateID`  | `INT`  | This identifies the date of the record and is associated with a date value in the date table  | 0-2,147,483,647 | This will save space over using strings for dates |
| `SolarWindSpeed`  | `REAL`  | This is a measurement of the solar wind speed in | Unsure | **Add Units** |
---

## General Dataset

### Dataset Summary
- **Dataset Name**: `General`
- **Description**:
- **Source**: All of this data was sourced from **TBD**. A link to the exact data source associated with each variable can be found in the [Notes and References](#notes-and-references) section.
- **Tables**: TBD
- **Number of Variables**: TBD
- **Number of Records**: TBD
- **Last Updated**: `2025-01-02`

---

### Variable Details

| Variable Name | Data Type  | Description                         | Allowed Values/Range     | Notes                          |
|---------------|------------|-------------------------------------|--------------------------|--------------------------------|
| `[TableName]ID`  | `INT`   | This is the unqiue identifier for each record  | 0-2,147,483,647 | This will be autoincremented starting at 0 | N/A |
| `DateID`  | `INT`  | This identifies the date of the record and is associated with a date value in the date table  | 0-2,147,483,647 | This will save space over using strings for dates |
| `SolarWindSpeed`  | `REAL`  | This is a measurement of the solar wind speed in | Unsure | **Add Units** |
---

## Notes and References
- **Data Collection Methodology**: Brief explanation of how the data was collected.
- **Transformations**: Any preprocessing steps applied to the data.
- **References**: Links or citations to original sources.

---

## Changelog
- **Version 1.0** (2024-01-02): Initial creation of the data dictionary.
