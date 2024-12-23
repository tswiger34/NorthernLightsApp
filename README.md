# Northern Lights Alert

Northern Lights Alert is an application designed to notify users about opportunities to view the Northern Lights. The app is being developed in three phases, each introducing new features to enhance the user experience and provide more functionality. The project leverages modern technologies for data collection, personalized reporting, and predictive modeling.

## Project Goals
- Provide timely alerts for aurora borealis viewing opportunities.
- Deliver personalized reports based on user preferences and weather conditions.
- Utilize predictive modeling to improve accuracy in forecasting viewing opportunities.

## Development Phases
### Phase 0: MVP Being Locally Hosted by Users
Key Features:
- Scrapes NOAA’s dashboard every 6 hours to check for a Kp index of 5 or higher.
- Sends alerts via email or SMS with the Kp level and forecasted date.
- Makefile to help people setup app to host on their local machines
  
Technology Stack:
- Python for backend development.
- Scheduler: APScheduler
- Alert System: MIME/SMTP for email
- User preferences stored in json files and .env file
### Phase 1: Fully Functional App

The MVP focuses on sending automated alerts when the NOAA (National Oceanic and Atmospheric Administration) forecasts a Kp index of 5 or higher, which indicates geomagnetic activity sufficient to view the Northern Lights in some locations.

Key Features:
- Scrapes NOAA’s dashboard every 6 hours to check for a Kp index of 5 or higher.
- Sends alerts via email or SMS with the Kp level and forecasted date.
- Reliable and lightweight backend to manage scheduling and alert distribution.

Technology Stack:
- Python for backend development.
- Scheduler: AWS Lambda
- Alert System: Twillio for SMS, MIME/SMTP for email
- Database: PostgreSQL through AWS

### Phase 2: Personalized Reports

In this phase, the app adds user-specific customization to the alerts, offering location-based recommendations for viewing the Northern Lights.

Key Features:
- User registration and profile management.
- A survey to capture user preferences, including location and driving radius.
- Recommendations for the top 5 viewing locations based on weather forecasts, Kp index, and user inputs.
- Integration with location services (e.g., Google Maps API) and weather data APIs.

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
- Big data storage and processing (e.g., AWS S3, Apache Spark).
- Visualization tools (e.g., Plotly Dash, Streamlit).

## General Infrastructure

### Tech Infrastructure
Cloud Hosting: AWS, Google Cloud, or Azure for scalability.
Database: SQLite for MVP; PostgreSQL or MySQL for later phases.
APIs: RESTful APIs for backend communication.
CI/CD: GitHub Actions or Jenkins for continuous integration and deployment.
Monitoring: Tools like New Relic or Sentry for application performance and error tracking.

### Version Control

The project is managed using Git with a public/private repository on GitHub.

## Getting Started
### Prerequisites
Python 3.8+
Node.js for frontend development (Phase 2+).
Access to NOAA’s dashboard and relevant APIs (OpenWeatherMap, Google Maps).

### Installation
Clone the repository:
git clone https://github.com/tswiger34/NorthernLightsApp.git

### Install dependencies:

- pip install -r requirements.txt
- Set up environment variables for API keys

### Run the application:

python app.py

### Future Plans

- Expand to include global aurora alerts
- Develop a mobile app for iOS and Android

### Contributing

We welcome contributions from the community! Please open an issue or submit a pull request to propose changes or new features.

# License

This project is licensed under the MIT License. See the LICENSE file for details.

# Acknowledgments

Special thanks to the NOAA for their open data and resources, and to all contributors and testers who help make this project a reality.
