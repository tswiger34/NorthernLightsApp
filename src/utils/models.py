from pydantic import BaseModel
from typing import List, Optional

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