import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from loguru import logger

from app.config import settings


class GoogleDriveBackup:
    """
    Google Drive backup using rclone with OAuth2 token.
    Service Accounts don't work with personal Google Drive - they require Workspace or paid GCS.
    OAuth2 token represents personal Google account and uses personal storage quota.
    """

    def __init__(self):
        self.gdrive_oauth_token = settings.GDRIVE_OAUTH_TOKEN
        self.gdrive_folder_path = settings.GDRIVE_FOLDER_PATH

    def _setup_rclone_config(self, config_path: Path) -> bool:
        """Create temporary rclone config with OAuth token."""
        if not self.gdrive_oauth_token:
            logger.warning("GDRIVE_OAUTH_TOKEN not configured, skipping Google Drive backup")
            return False

        try:
            config_content = f"""[gdrive]
type = drive
scope = drive
token = {self.gdrive_oauth_token}
"""
            config_path.write_text(config_content)
            logger.debug(f"rclone config created at {config_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to setup rclone config: {e}")
            return False

    def upload_to_gdrive(self, file_path: str) -> bool:
        """Upload backup file to Google Drive using rclone."""

        # Create temporary config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.conf', delete=False) as tmp_config:
            config_path = Path(tmp_config.name)

        try:
            if not self._setup_rclone_config(config_path):
                return False

            file_path = Path(file_path)
            if not file_path.exists():
                logger.error(f"Backup file not found: {file_path}")
                return False

            # Build rclone command
            cmd = [
                "rclone", "copy",
                str(file_path),
                f"gdrive:{self.gdrive_folder_path}/",
                "--config", str(config_path),
                "-v"
            ]

            logger.info(f"Uploading {file_path.name} to Google Drive...")

            # Execute rclone
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )

            if result.returncode == 0:
                logger.info(f"Successfully uploaded {file_path.name} to Google Drive")
                if result.stdout:
                    logger.debug(f"rclone output: {result.stdout}")
                return True
            else:
                logger.error(f"rclone failed with code {result.returncode}")
                if result.stderr:
                    logger.error(f"rclone error: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            logger.error("rclone upload timed out after 5 minutes")
            return False
        except Exception as e:
            logger.error(f"Failed to upload to Google Drive: {e}")
            return False
        finally:
            # Clean up temporary config
            try:
                if config_path.exists():
                    config_path.unlink()
                    logger.debug("Temporary rclone config cleaned up")
            except Exception as e:
                logger.error(f"Failed to cleanup temp config: {e}")

    def list_backups(self) -> Optional[list]:
        """List backups in Google Drive folder."""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.conf', delete=False) as tmp_config:
            config_path = Path(tmp_config.name)

        try:
            if not self._setup_rclone_config(config_path):
                return None

            cmd = [
                "rclone", "lsjson",
                f"gdrive:{self.gdrive_folder_path}/",
                "--config", str(config_path),
                "--max-depth", "1"
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                import json
                files = json.loads(result.stdout)
                backups = []

                for file_info in files:
                    if not file_info.get("IsDir", False):
                        file_name = file_info.get("Name", "")
                        if file_name.endswith((".sql", ".sql.gz", ".sql.zip")):
                            backups.append({
                                "name": file_name,
                                "size": file_info.get("Size", 0),
                                "modified": file_info.get("ModTime", "")
                            })

                return sorted(backups, key=lambda x: x["modified"], reverse=True)
            else:
                logger.error(f"Failed to list Google Drive backups: {result.stderr}")
                return None

        except Exception as e:
            logger.error(f"Failed to list Google Drive backups: {e}")
            return None
        finally:
            try:
                if config_path.exists():
                    config_path.unlink()
            except Exception as e:
                logger.error(f"Failed to cleanup temp config: {e}")

    def check_rclone_installed(self) -> bool:
        """Check if rclone is installed and accessible."""
        try:
            result = subprocess.run(
                ["rclone", "version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                logger.debug(f"rclone is installed: {result.stdout.split()[2]}")
                return True
            return False
        except (subprocess.SubprocessError, FileNotFoundError):
            logger.error("rclone is not installed or not in PATH")
            return False