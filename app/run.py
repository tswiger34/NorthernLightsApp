from app.main import *
import time
from threading import Thread, Event

# Event to signal when to stop the thread
stop_event = Event()

def run_alerts():
    while not stop_event.is_set():
        NLApp()
        time.sleep(86400)

if __name__ == "__main__":
    try:
        # Start the thread
        alert_thread = Thread(target=run_alerts, daemon=True)
        alert_thread.start()

        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        stop_event.set()
        alert_thread.join()

    