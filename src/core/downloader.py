"""YouTube downloader using yt-dlp."""
import logging
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, Optional, cast

import yt_dlp
from yt_dlp.utils import DownloadError

from src.services.config import config
from src.core.validators import is_playlist_url


class DownloadQuality(Enum):
    """Available download quality options."""
    BEST = "best"
    HIGH = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
    MEDIUM = "bestvideo[height<=720]+bestaudio/best[height<=720]"
    LOW = "bestvideo[height<=480]+bestaudio/best[height<=480]"
    AUDIO_BEST = "bestaudio/best"
    AUDIO_MP3 = "bestaudio[ext=m4a]"


class DownloadType(Enum):
    """Type of download."""
    VIDEO = "video"
    AUDIO = "audio"


def _progress_hook(
        callback: Optional[Callable[[Dict[str, Any]], None]]
) -> Callable[[Dict[str, Any]], None]:
    """Create a progress hook for yt-dlp.

    Args:
        callback: User callback to invoke with progress updates

    Returns:
        Progress hook function
    """

    def hook(d: Dict[str, Any]) -> None:
        if callback:
            callback(d)

    return hook


class Downloader:
    """YouTube downloader wrapper for yt-dlp."""

    QUALITY_PRESETS: Dict[str, str] = {
        "Mejor calidad": DownloadQuality.BEST.value,
        "Alta (1080p)": DownloadQuality.HIGH.value,
        "Media (720p)": DownloadQuality.MEDIUM.value,
        "Baja (480p)": DownloadQuality.LOW.value,
        "Audio mejor calidad": DownloadQuality.AUDIO_BEST.value,
        "Audio MP3": DownloadQuality.AUDIO_MP3.value,
    }

    def __init__(
            self,
            output_dir: Optional[Path] = None,
            logger: Optional[logging.Logger] = None
    ) -> None:
        """Initialize the downloader.

        Args:
            output_dir: Directory to save downloads
            logger: Logger instance
        """
        self.output_dir = output_dir or config.downloads_dir
        self.logger = logger or logging.getLogger(__name__)
        self._current_download: Optional[str] = None

    def download(
            self,
            url: str,
            quality: str = "Mejor calidad",
            download_type: DownloadType = DownloadType.VIDEO,
            progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
            error_callback: Optional[Callable[[str], None]] = None
    ) -> bool:
        """Download a video or audio from YouTube.

        Args:
            url: YouTube URL to download
            quality: Quality preset name
            download_type: Type of download (video or audio)
            progress_callback: Callback for progress updates
            error_callback: Callback for errors

        Returns:
            True if download succeeded, False otherwise
        """
        try:
            self._current_download = url
            format_string = self.QUALITY_PRESETS.get(quality, DownloadQuality.BEST.value)

            ydl_opts: Any = {
                "format": format_string,
                "outtmpl": str(self.output_dir / "%(title)s.%(ext)s"),
                "progress_hooks": [_progress_hook(progress_callback)],
                "logger": self.logger,
                "quiet": True,
                "no_warnings": True,
                "writethumbnail": True,
                "embedthumbnail": True,
            }

            if download_type == DownloadType.AUDIO:
                ydl_opts["postprocessors"] = [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    },
                    {
                        "key": "EmbedThumbnail",
                        "already_have_thumbnail": False,
                    },
                    {
                        "key": "FFmpegMetadata",
                        "add_metadata": True,
                    }
                ]
            else:
                ydl_opts["postprocessors"] = [
                    {
                        "key": "EmbedThumbnail",
                        "already_have_thumbnail": False,
                    }
                ]

            if is_playlist_url(url):
                ydl_opts["noplaylist"] = False
                self.logger.info(f"Downloading playlist: {url}")
            else:
                ydl_opts["noplaylist"] = True
                self.logger.info(f"Downloading single video: {url}")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.logger.info(f"Successfully downloaded: {url}")
            return True

        except DownloadError as e:
            error_msg = f"Download error: {str(e)}"
            self.logger.error(error_msg)
            if error_callback:
                error_callback(error_msg)
            return False

        except Exception as e:
            error_msg = f"Unexpected error during download: {str(e)}"
            self.logger.exception(error_msg)
            if error_callback:
                error_callback(error_msg)
            return False

        finally:
            self._current_download = None

    def get_video_info(self, url: str) -> Optional[Dict[str, Any]]:
        """Get information about a video without downloading.

        Args:
            url: YouTube URL

        Returns:
            Video information dictionary or None on error
        """
        try:
            ydl_opts: Any = {
                "quiet": True,
                "no_warnings": True,
                "extract_flat": True if is_playlist_url(url) else False,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return cast(Dict[str, Any], cast(object, info)) if info else None

        except Exception as e:
            self.logger.error(f"Error getting video info: {str(e)}")
            return None
