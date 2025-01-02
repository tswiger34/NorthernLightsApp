# Overview
The NorthernLights Alerts App comprises a backend system for data aggregation and analysis, and a notification system for delivering alerts to users. It uses web scraping to retrieve periodic Kp forecasts to notify users if the Northern Lights will be visible.

# Diagram
To be done later

# Core Components
## Data
### Forecast Data
- KP Index: Gathers 3-day Kp index forecasts from NOAA every 6 hours to inform automated alerts. This is then stored in a SQLite database for future use in the recommendation systems
- Weather: Scrapes 3-day weather forecasts from Open-Meteo for important weather factors to be used in the recommendation system. This is also stored in a SQLite database
### Historical/Live Data
- Solar Weather: Collected from NOAAs open data, stored in a SQLite database to train models for recommendation system

- Solar Wind Hist (Minute): https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind.json
- Solar Mag Hist (Minute): https://services.swpc.noaa.gov/products/solar-wind/mag-7-day.json
- 7-Day Plasma Hist (Minute): https://services.swpc.noaa.gov/products/solar-wind/plasma-7-day.json
- Aurora Info North Forecast (Minute): https://services.swpc.noaa.gov/text/ovation_latest_aurora_n.txt
- Aurora Info South Forecast (Minute): https://services.swpc.noaa.gov/text/ovation_latest_aurora_s.txt
- Kp Historical Detailed (3-hours): https://services.swpc.noaa.gov/text/daily-geomagnetic-indices.txt
- Kp Forecasts Detailed (3-hours): https://services.swpc.noaa.gov/text/3-day-solar-geomag-predictions.txt
- Solar Indices Historical (Daily): https://services.swpc.noaa.gov/text/daily-solar-indices.txt
- Geo Scales (Daily): https://services.swpc.noaa.gov/products/noaa-scales.json
- Radio Flux Obs (Daily): https://services.swpc.noaa.gov/products/10cm-flux-30-day.json
- Sunspots (Daily): https://services.swpc.noaa.gov/json/sunspot_report.json
- Aurora Outcomes: https://www.aurorasaurus.org/

- Earth Weather: Collected from Open-Meteo and stored in a SQLite database to train models for recommendation system
- Moon Phases: This is collected from https://www.timeanddate.com/moon/phases/ and stored in a SQLite database to be used in recommendation models
- Artificial Light Pollution Estimates: https://www.nps.gov/subjects/nightskies/datacollectionsites.htm
- Viewing Location GIS Data: Google Maps and TheDyrt
- View Quality: News/Blog reports stored in BLOB storage, sentiment scores and metadata stored in SQLite
### Scripts
- This is where all of the web scraping scripts/api call scripts will be held
## App
- Alerts: Manages all of the alerts for the app
- Data Scraping: Scrapes data required to inform the alerts/recommendation system
- Recommendation System: This is where the inference scripts and models for the recommendation system will be held
- Utils: This is where miscellaneous scripts will be held to run the app
- main.py: holds the core functionallity for the app
- run.py: This sets up the script to run in the background every 6 hours
## Logs
- This holds all of the log reports for debugging
## Recommendation System
- This will include all of the data engineering, model training, and behavior logic for the recommendation system
## Tests
- This includes all of the necessary unit and integration tests
## Makefile
- For now this will allow for others to host a local instance of this script on their own machine

# Dataflow
Kp Index Forecast: API request to NOAA -> Data Processing -> Store as txt file -> Analyze Data -> Send alerts if triggered
User Preferences: Stored in .env file on build -> Fetched during CreateAlerts -> Informs Alert Types -> Used to send alert

# Tech Stack
- Backend: Python, Java
- Frontend: React.js
- Database: SQLite
- CI/CD: MLFlow and DVC for recommendation models, GitHub Actions for backend and front end
- View Probability Models: SciKit Learn
- Sentiment Scoring: Hugging Face Models