import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "itairs.log")


def setup_logging():
  logger = logging.getLogger("itairs")
  logger.setLevel(logging.INFO)

  formatter = logging.Formatter(
      "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
  )

  handler = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=3)
  handler.setFormatter(formatter)
  logger.addHandler(handler)

  stream = logging.StreamHandler()
  stream.setFormatter(formatter)
  logger.addHandler(stream)

  return logger
