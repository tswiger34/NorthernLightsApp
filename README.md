# Northern Lights Alert

Northern Lights Alert is an application designed to notify users about opportunities to view the Northern Lights. The app is being developed in four phases, each introducing new features to enhance the user experience and provide more functionality. The project leverages modern technologies for data collection, personalized reporting, and predictive modeling.

## Project Goals
- Provide timely alerts for viewing opportunities
- Create a trip recommender system based on user preferences and weather conditions
- Utilize predictive modeling to improve accuracy in forecasting viewing opportunities

## Development Phases
### Phase 0: MVP Being Locally Hosted by Users
The MVP focuses on sending automated alerts when the NOAA (National Oceanic and Atmospheric Administration) forecasts a Kp index of 5 or higher, which indicates geomagnetic activity sufficient to view the Northern Lights in some locations. The goal of this is to essentially just get this out the door.

Key Features:
- Scrapes NOAA’s dashboard every 6 hours to check for a Kp index of 5 or higher.
- Sends alerts via email or SMS with the Kp level and forecasted date.
- Makefile for testers to implement the alerts system on their local machine
- Extremely lightweight app with only the core functionality of sending alerts available
  
Technology Stack:
- Python for backend development.
- Scheduler: APScheduler
- Alert System: MIME/SMTP for email
- User preferences stored in json files and .env file
### Phase 1: Optimize and Improve Core Functionality
Phase 1 will look to create a significantly improved version of phase 0 along with setup the infrastructure for Phase 2 and 3. This will include conversion of the Python code will be converted to Java, Phase 0 methods will be time optimized, functionality added to the alerts system, and protect against edge cases in the data scraper, and data collection methods for recommender/prediction models will be created.

Key Features:
- Alerts for if the NOAA Kp forecast data format has changed
- SMS alerts functionality
- Java implementations of core features
- Improved test coverage of core features
- SQLite database setup to store Earth weather, solar weather, and moon phase information
- Data scraper for solar weather forecasts and earth weather forecasts
- Data scraper for historical/actual solar weather, Kp index, earth weather, and moon phases

Technology Stack:
- Java for backend development of app
- Python for aggregation methods
- Scheduler: APScheduler
- Alert System: Twillio for SMS, MIME/SMTP for email
- Databases: SQLite hosted on local machine
- APIs: Earth Weather historical/forecasts, Moon Phases, and Historical Solar Weather TBD

### Phase 2: Personalized Reports

In this phase, the app adds user-specific customization to the alerts, offering location-based recommendations for viewing the Northern Lights.

Key Features:
- User registration and profile management.
- A survey to capture user preferences, including location and driving radius.
- Recommendations for the top 5 viewing locations based on weather forecasts, Kp index, and user inputs.
- Integration with location services such as Google Maps and TheDyrt and weather data APIs.

Technology Stack Additions:
- React.js for the frontend interface.
- Database: PostgreSQL hosted with cloud provider TBD
- APIs: Weather and Location APIs TBD
- Authentication: Firebase

### Phase 3: Predictive Modeling

The final phase introduces proprietary predictive modeling to improve the accuracy of viewing recommendations.

Key Features:
- Collects and processes data from historical Kp levels, other solar weather measurements, weather conditions, and geo-coordinates of successful sightings
- Uses machine learning models to predict the likelihood of viewing the Northern Lights in specific locations.
- Enhances personalized reports with more precise and reliable predictions.

Technology Stack Additions:
- Machine learning frameworks, most likely SciKit Learn
- Data pipeline tools TBD
- Visualization tools TBD

## General Infrastructure

### Tech Infrastructure
Cloud Hosting: AWS, Google Cloud, or Azure for scalability
Database: SQLite for MVP; PostgreSQL for later phases
APIs: TBD
CI/CD: GitHub Actions for CI/CD of code infrastructure, DVC and MLFlow for predictive modeling
Monitoring: Tools like New Relic or Sentry for application performance and error tracking

### Version Control

The project is managed using Git with a public repository on GitHub.

## Getting Started
### Prerequisites
Python 3.8+
Node.js for frontend development (Phase 2+).
Access to NOAA’s dashboard

### Installation
Clone the repository:
git clone https://github.com/tswiger34/NorthernLightsApp.git

### Install dependencies:

- pip install -r requirements.txt
- Set up environment variables for API keys

### Run the application:

python app.py

### Future Plans

- Expand to include international alerts

### Contributing

We welcome contributions from the community! Please open an issue or submit a pull request to propose changes or new features.

# Current Status
This project is currently in phase 0, and is roughly halfway to completetion of this phase. Current tasks in progress as of 12/23/2024 are:
- Improved logging for debugging
- Scheduler functionality
- Unit tests for alerts and Kp forecast scraping
- Integration testing of core functions

# License

This project is licensed under the MIT License. See the LICENSE file for details.

# Acknowledgments

Special thanks to the NOAA for their open data and resources
