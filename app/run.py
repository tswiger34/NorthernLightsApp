from app.main import *
import time
from threading import Thread

def run_alerts():
    while True:
        NLApp()
        time.sleep(60)

if __name__ == "__main__":
    Thread(target=run_alerts, daemon=True).start()
    