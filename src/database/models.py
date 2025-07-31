from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.database.connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime)

    alerts = relationship("Alert", back_populates="owner")


class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    pressure = Column(Float)
    timestamp = Column(DateTime)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    alert_type = Column(String)
    threshold = Column(Float)
    created_at = Column(DateTime)

    owner = relationship("User", back_populates="alerts")
