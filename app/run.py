from app.main import *
import schedule

def run_alerts():
    alerts = NLApp()

schedule.every(6).hours.do(run_alerts)

while True:
    schedule.run_pending()
    time.sleep(1)