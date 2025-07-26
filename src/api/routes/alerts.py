from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from src.alerts.manager import AlertManager

router = APIRouter()
alert_manager = AlertManager()

class Alert(BaseModel):
    id: int
    message: str
    severity: str
    is_active: bool

@router.post("/alerts/", response_model=Alert)
async def create_alert(alert: Alert):
    try:
        return alert_manager.create_alert(alert)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/alerts/", response_model=List[Alert])
async def get_alerts():
    try:
        return alert_manager.get_alerts()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/alerts/{alert_id}", response_model=Alert)
async def get_alert(alert_id: int):
    try:
        return alert_manager.get_alert(alert_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/alerts/{alert_id}", response_model=Alert)
async def update_alert(alert_id: int, alert: Alert):
    try:
        return alert_manager.update_alert(alert_id, alert)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/alerts/{alert_id}", response_model=dict)
async def delete_alert(alert_id: int):
    try:
        alert_manager.delete_alert(alert_id)
        return {"message": "Alert deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))