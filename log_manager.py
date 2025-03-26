import logging

logging.basicConfig(filename="system.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def log_event(message):
    logging.info(message)

def log_error(message):
    logging.error(message)

def log_warning(message):
    logging.warning(message)
