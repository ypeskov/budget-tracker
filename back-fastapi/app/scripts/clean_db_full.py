import sys
from pathlib import Path

from sqlalchemy import text

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

from app.database import engine  # noqa
from app.logger_config import logger  # noqa

logger.info("🧹 Cleaning DB...")
with engine.connect() as conn:
    conn.execute(text("DROP SCHEMA public CASCADE"))
    conn.execute(text("CREATE SCHEMA public"))
    conn.commit()

logger.info("✅ DB fully wiped and public schema recreated")
