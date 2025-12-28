"""Constants and utilities for the application."""

# Application constants
APP_NAME = "YouTube Download"
APP_VERSION = "1.0.0"
APP_AUTHOR = "YouTube Download Team"

# File extensions
VIDEO_EXTENSIONS = [".mp4", ".mkv", ".webm", ".avi", ".mov"]
AUDIO_EXTENSIONS = [".mp3", ".m4a", ".opus", ".wav"]

# Download settings
DEFAULT_MAX_CONCURRENT = 3
DEFAULT_TIMEOUT = 300  # 5 minutes


def sanitize_filename(filename: str) -> str:
    """Sanitize a filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


def format_bytes(bytes_value: int) -> str:
    """Format bytes to human-readable string.
    
    Args:
        bytes_value: Number of bytes
        
    Returns:
        Formatted string (e.g., "1.5 GB")
    """
    value = float(bytes_value)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if value < 1024.0:
            return f"{value:.1f} {unit}"
        value /= 1024.0
    return f"{value:.1f} PB"


def format_speed(speed_bps: float) -> str:
    """Format download speed to human-readable string.
    
    Args:
        speed_bps: Speed in bytes per second
        
    Returns:
        Formatted string (e.g., "2.5 MB/s")
    """
    return f"{format_bytes(int(speed_bps))}/s"


def format_time(seconds: float) -> str:
    """Format time in seconds to human-readable string.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted string (e.g., "2h 30m 15s")
    """
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"
