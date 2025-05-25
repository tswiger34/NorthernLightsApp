from utils.logging_config import setup_logging

def main():
    # Initialize logging
    logger = setup_logging()
    logger.info("Starting Northern Lights Alert application.")

    try:
        logger.debug("Fetching NOAA forecast data.")
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()