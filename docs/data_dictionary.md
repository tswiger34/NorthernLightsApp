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
- **Number of Tables**: 6
- **Number of Variables**: 63
- **Last Updated**: `2025-01-02`

---

### Variable Details

| Variable Name | Data Type | Description                         | Allowed Values/Range     | Notes                          |
|---------------|------------|-------------------------------------|--------------------------|--------------------------------|
| `[TableName]WeatherID`  | `INT` | This is the unqiue identifier for each record | 0-2,147,483,647 | This will be autoincremented starting at 0 | Found in all tables |
| `DateID`  | `INT` | This identifies the date of the record and is associated with a date value in the date table | Unsure | This will save space over using strings for dates, found in all tables |
| `SolarWindSpeed` | `REAL` | This is a measurement of the solar wind speed in **Add Units** | Unsure | Minute table |
| `SolarWindDensity` | `REAL` | This is a measurement of the solar wind density in **Add Units** | Unsure | Minute table |
| `SolarWindTemp` | `INT` | This is a measurement of the solar wind temperature in **Add Units** | Unsure | Minute table |
| `SolarWindby` | `REAL` | This represents the y component of the solar wind axis | Unsure | Minute table |
| `SolarWindbx` | `REAL` | This represents the x component of the solar wind axis | Unsure | Minute table |
| `SolarWindbz` | `REAL` | This represents the z component of the solar wind axis | Unsure | Minute table |
| `SolarWindbt` | `REAL` | This represents the time component of the solar wind axis | Unsure | Minute table |
| `SolarWindby_gsm` | `REAL` | This represents the y component of the solar wind axis | Unsure | Minute table |
| `SolarWindbx_gsm` | `REAL` | This represents the x component of the solar wind axis | Unsure | Minute table |
| `SolarWindbz_gsm` | `REAL` | This represents the z component of the solar wind axis | Unsure | Minute table |
| `SolarWindbt_gsm ` | `REAL` | This represents the time component of the solar wind axis | Unsure | Minute table |
| `PlasmaSpeed` | `REAL` | This is a measurement of the plasma speed in **Add Units** | Unsure | Minute table |
| `PlasmaDensity` | `REAL` | This is a measurement of the plasma density in **Add Units** | Unsure | Minute table |
| `PlasmaTemp` | `INT` | This is a measurement of the plasma temperature in **Add Units** | Unsure | Minute table |
| `Time` | `TINYINT` | This represents the time of a measurement in an int representation of military time | Unsure | Hourly observed and forecasted tables |
| `Latitude Prefixes` | `N/A` | The prefixes can either be `Hi` or `Mid` to represent whether the observation or forecast was made. `Hi` represents Fredricksburg, VA and `Mid` represents Boulder, CO | N/A | Hourly observed and forecasted tables |
| `[Latitude Prefix]KpIndex` | `REAL` | This is a measuremoent or forecast of the planetary K-index | Unsure | Hourly observed and forecasted tables |
| `[Latitude Prefix]KpIndex` | `REAL` | This is a measuremoent or forecast of the planetary A-index | Unsure | Hourly observed and forecasted tables |
| `[Latitude Prefix]Active` | `TINYINT` | NOAA predicted probability of an active Aurora Borealis status at or above given latitude | 0-100 | Hourly forecasted table |
| `[Latitude Prefix]Minor` | `TINYINT` | NOAA predicted probability of an minor Aurora Borealis storm at or above given latitude | 0-100 | Hourly observed and forecasted tables |
| `[Latitude Prefix]Major` | `TINYINT` | NOAA predicted probability of an major Aurora Borealis storm at or above given latitude | 0-100 | Hourly forecasted table |
| `AbsorbtionForecast` | `VARCHAR(20)` | NOAA predicted color absoption, i.e. `green`. Gives an idea of what color the Northern Lights will be | N/A | Hourly forecasted tables |
| `MFlareProb` | `TINYINT` | NOAA predicted probability of an M-Class flare being emitted | 0-100 | Hourly forecasted tables |
| `XFlareProb` | `TINYINT` | NOAA predicted probability of an X-Class flare being emitted | 0-100 | Hourly forecasted tables |
| `ProtonFlareProb` | `TINYINT` | NOAA predicted probability of an Proton flare being emitted | 0-100 | Hourly forecasted tables |
| `RadioFlux` | `TINYINT` | Measured/forecasted 10.7cm radio flux at noon UTC | Unsure | Hourly observed and forecasted tables |
| `MaxKp` | `REAL` | Maximum observed/forecasted plantary-K index throughout the day | 0-9 | Daily observed and forecasted tables |
| `MaxAp` | `TINYINT` | Maximum observed/forecasted plantary-A index throughout the day | Unsure | Daily observed and forecasted tables |
| `MaxRadioFlux` | `TINYINT` | Maximum measured/forecasted 10.7cm radio flux at noon UTC | Unsure | Daily observed and forecasted tables |
| `ObsID` | `INT` | Observation ID as given by NOAA for sunspots. The same sunspot may be observed by different observatories or at different times, so each observations has a unique ID | Unsure | Sun Spots table |
| `Observatory` | `VARCHAR(10)` | Name of the observatory that made the observation | Unsure | Sun Spots table |
| `Type` | `VARCHAR(10)` | Type of sunspot observed | Unsure | Sun Spots table |
| `Quality` | `TINYINT` | Quality of the observation, higher value measn worse quality | Unsure | Sun Spots table |
| `Region` | `SMALLINT` | Region of the sun where the sun spot was observed | Unsure | Sun Spots table |
| `Latitude` | `REAL` | Solar latitude where the sun spot was observed | Unsure | Sun Spots table |
| `Longited` | `REAL` | Solar longitude where the sun spot was observed | Unsure | Sun Spots table |
| `Location` | `VARCHAR(10)` | More precise location of the sun where the sun spot was observed than `Region`, but not as precise as `Longitude`/`Latitude` | N/A | Sun Spots table |
| `Class` | `VARCHAR(10)` | Class of flare emitted if any, this has to do with types of particles emitted | Unsure | Sun Spots table |
| `Magnitude` | `VARCHAR(10)` | Magnitude of flare emitted if any, a large flare size leads to a higher probabilty of viewing the Northern Lights | Unsure | Sun Spots table |
| `Numspot` | `TINYINT` | Unsure | Unsure | Sun Spots table |
| `Compact` | `TINYINT` | Unsure | Unsure | Sun Spots table |

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
| `SolarWindSpeed`  | `REAL` | This is a measurement of the solar wind speed in | Unsure | **Add Units** |
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
- **Data Collection Methodology**:
    - *Solar Weather*: Webscraping NOAA's publicly accessible data, see data/solarweather.py for code to scrape data.
    - *Earth Weather*: **TBD**
    - *Lunar Features*: Webscraped from TimeandDate.com's publicly accessible data. See data/lunardata.py for code used to scrape the data.
- **Transformations**: Any preprocessing steps applied to the data
    - Convert date and times from PST to UTC for lunar features
    - Estimation method for moon luminosity can be found in data/general.py

- **References**: Links to original sources.
    1. Solar Wind Hist (Minute): https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind.json
    2. Solar Mag Hist (Minute): https://services.swpc.noaa.gov/products/solar-wind/mag-7-day.json
    3. 7-Day Plasma Hist (Minute): https://services.swpc.noaa.gov/products/solar-wind/plasma-7-day.json
    4. Kp Historical Detailed (3-hours): https://services.swpc.noaa.gov/text/daily-geomagnetic-indices.txt
    5. Kp Forecasts Detailed (3-hours): https://services.swpc.noaa.gov/text/3-day-solar-geomag-predictions.txt
    6. Solar Indices Historical (Daily): https://services.swpc.noaa.gov/text/daily-solar-indices.txt
    7. Geo Scales (Daily): https://services.swpc.noaa.gov/products/noaa-scales.json
    8. Radio Flux Obs (Daily): https://services.swpc.noaa.gov/products/10cm-flux-30-day.json
    9. Sunspots (Daily): https://services.swpc.noaa.gov/json/sunspot_report.json
- **Link to ERD**: **TBD**
---

## Changelog
- **Version 1.0** (2025-01-02): Initial creation of the data dictionary.
