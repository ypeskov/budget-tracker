import os

from loguru import logger

from app.config import Settings

settings = Settings()

logger.add("logs/debug.log", level="DEBUG", rotation="1 week", compression="zip")
logger.add("logs/info.log", level="INFO", rotation="1 week", compression="zip")
logger.add("logs/error.log", level="ERROR", rotation="1 week", compression="zip")

if "TEST_MODE" in os.environ:
    logger.remove()
    logger.add(f"logs/{settings.TEST_LOG_FILE}", level="DEBUG", rotation="1 week", compression="zip")
