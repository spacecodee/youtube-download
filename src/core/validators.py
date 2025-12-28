"""URL validation utilities."""
import re
from typing import Tuple


def validate_youtube_url(url: str) -> Tuple[bool, str]:
    """Validate if a URL is a valid YouTube URL.

    Args:
        url: URL to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not url or not url.strip():
        return False, "URL cannot be empty"

    youtube_patterns = [
        r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$",
        r"^(https?://)?(music\.youtube\.com)/.+$"
    ]

    for pattern in youtube_patterns:
        if re.match(pattern, url, re.IGNORECASE):
            return True, ""

    return False, "Not a valid YouTube or YouTube Music URL"


def is_playlist_url(url: str) -> bool:
    """Check if a URL is a playlist URL.

    Args:
        url: URL to check

    Returns:
        True if the URL is a playlist
    """
    return "list=" in url.lower() or "/playlist" in url.lower()
