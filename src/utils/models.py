from pydantic import BaseModel
from typing import List, Optional
import pandas as pd


class User(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool


class WeatherData(BaseModel):
    temperature: float
    humidity: float
    wind_speed: float
    description: str


class Alert(BaseModel):
    id: int
    user_id: int
    alert_type: str
    message: str
    is_active: bool


class GeoWeatherData(BaseModel):
    latitude: float
    longitude: float
    weather: WeatherData


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None


class AlertCreate(BaseModel):
    user_id: int
    alert_type: str
    message: str


class AlertUpdate(BaseModel):
    alert_type: Optional[str] = None
    message: Optional[str] = None
    is_active: Optional[bool] = None


class WeatherResponse(BaseModel):
    data: List[WeatherData]


class DayForecast(BaseModel):
    date: str
    time_00_03: str
    time_03_06: str
    time_06_09: str
    time_09_12: str
    time_12_15: str
    time_15_18: str
    time_18_21: str
    time_21_00: str


class ThreeDayForecast(BaseModel):
    day_1: DayForecast
    day_2: DayForecast
    day_3: DayForecast

    def to_dataframe(self) -> pd.DataFrame:
        """
        Converts the ThreeDayForecast to a DataFrame with dates as columns and times as rows.

        Returns:
            pd.DataFrame: DataFrame with time periods as index and dates as columns
        """
        # Define the time periods in order
        time_periods = ["00-03", "03-06", "06-09", "09-12", "12-15", "15-18", "18-21", "21-00"]

        data = {
            self.day_1.date: [
                self.day_1.time_00_03,
                self.day_1.time_03_06,
                self.day_1.time_06_09,
                self.day_1.time_09_12,
                self.day_1.time_12_15,
                self.day_1.time_15_18,
                self.day_1.time_18_21,
                self.day_1.time_21_00,
            ],
            self.day_2.date: [
                self.day_2.time_00_03,
                self.day_2.time_03_06,
                self.day_2.time_06_09,
                self.day_2.time_09_12,
                self.day_2.time_12_15,
                self.day_2.time_15_18,
                self.day_2.time_18_21,
                self.day_2.time_21_00,
            ],
            self.day_3.date: [
                self.day_3.time_00_03,
                self.day_3.time_03_06,
                self.day_3.time_06_09,
                self.day_3.time_09_12,
                self.day_3.time_12_15,
                self.day_3.time_15_18,
                self.day_3.time_18_21,
                self.day_3.time_21_00,
            ],
        }

        df = pd.DataFrame(data, index=time_periods)
        df.index.name = "Time Period (UTC)"

        return df

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool