from fastapi import APIRouter, HTTPException
from typing import List
from src.database.models import WeatherData
from src.database.connection import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/weather", response_model=List[WeatherData])
def get_weather_data(db: Session = next(get_db())):
    weather_data = db.query(WeatherData).all()
    if not weather_data:
        raise HTTPException(status_code=404, detail="No weather data found")
    return weather_data

@router.post("/weather", response_model=WeatherData)
def create_weather_data(weather: WeatherData, db: Session = next(get_db())):
    db.add(weather)
    db.commit()
    db.refresh(weather)
    return weather

@router.delete("/weather/{weather_id}", response_model=dict)
def delete_weather_data(weather_id: int, db: Session = next(get_db())):
    weather = db.query(WeatherData).filter(WeatherData.id == weather_id).first()
    if not weather:
        raise HTTPException(status_code=404, detail="Weather data not found")
    db.delete(weather)
    db.commit()
    return {"detail": "Weather data deleted successfully"}