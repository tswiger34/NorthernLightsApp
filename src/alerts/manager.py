from sqlalchemy.orm import Session
from src.database.models import Alert
from src.utils.models import AlertCreate, AlertUpdate
from src.database.connection import get_db
class AlertManager:
    def __init__(self):
        self.db:Session = get_db()

    def create_alert(self, alert_data: AlertCreate) -> Alert:
        new_alert = Alert(**alert_data.model_dump())
        self.db.add(new_alert)
        self.db.commit()
        self.db.refresh(new_alert)
        return new_alert

    def get_alert(self, alert_id: int) -> Alert:
        return self.db.query(Alert).filter(Alert.id == alert_id).first()

    def update_alert(self, alert_id: int, alert_data: AlertUpdate) -> Alert:
        alert = self.get_alert(alert_id)
        if alert:
            for key, value in alert_data.model_dump(exclude_unset=True).items():
                setattr(alert, key, value)
            self.db.commit()
            self.db.refresh(alert)
        return alert

    def delete_alert(self, alert_id: int) -> bool:
        alert = self.get_alert(alert_id)
        if alert:
            self.db.delete(alert)
            self.db.commit()
            return True
        return False

    def get_all_alerts(self) -> list[Alert]:
        return self.db.query(Alert).all()