import logging
import os

def setup_logging(log_file="northern_lights_app.log"):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(os.path.join(log_dir, log_file)),
            logging.StreamHandler()
        ]
    )

    # Return the root logger
    return logging.getLogger()