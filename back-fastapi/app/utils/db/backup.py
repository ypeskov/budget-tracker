import os
import subprocess
from datetime import datetime
from pathlib import Path

from icecream import ic

from app.logger_config import logger

ic.configureOutput(includeContext=True)


def backup_postgres_db(env_name: str,
                       host: str,
                       port: int,
                       dbname: str,
                       user: str,
                       password: str,
                       backup_dir: Path) -> bool:
    """ Create a backup of a PostgreSQL database """
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    backup_file = f"{backup_dir}/{env_name}-{dbname}_{timestamp}.sql"

    command = [
        "pg_dump",
        "-h", host,
        "-U", user,
        "-d", dbname,
        "-F", "p",
        "-f", backup_file
    ]

    environment = os.environ.copy()
    environment["PGPASSWORD"] = password

    try:
        subprocess.run(command,
                       env=environment,
                       check=True,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       text=True)
        logger.info(f"Backup of DB [{dbname}] is successfully created: {backup_file}")

        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error creating backup of DB [{dbname}]: {e.stderr}")
        # raise e
    except Exception as e:
        logger.error(e.strerror)
        # raise e
