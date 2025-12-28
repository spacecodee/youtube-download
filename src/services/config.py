"""Configuration management for the application."""
import os
from pathlib import Path
from typing import Optional


class Config:
    """Application configuration manager."""

    def __init__(self) -> None:
        """Initialize configuration with environment variables and defaults."""
        self.downloads_dir: Path = Path(
            os.getenv("DOWNLOADS_DIR", str(Path.home() / "Downloads" / "YouTube"))
        )
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        self.database_path: Path = Path(
            os.getenv("DATABASE_PATH", "./app_data/downloads.db")
        )
        self.max_concurrent_downloads: int = int(
            os.getenv("MAX_CONCURRENT_DOWNLOADS", "3")
        )

        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        self.downloads_dir.mkdir(parents=True, exist_ok=True)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)

    def get_download_path(self, filename: Optional[str] = None) -> Path:
        """Get the full path for a download.

        Args:
            filename: Optional filename to append to downloads directory

        Returns:
            Full path for the download
        """
        if filename:
            return self.downloads_dir / filename
        return self.downloads_dir


config = Config()
