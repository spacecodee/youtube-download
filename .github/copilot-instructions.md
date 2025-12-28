# Copilot Instructions

This document guides AI coding agents to be immediately productive in the YouTube Download application codebase.

## Project Overview

**YouTube Download** is a cross-platform desktop application (Windows, Linux, macOS) for downloading YouTube music and videos. Built with Python, it provides a user-friendly interface for batch downloading with customizable quality options.

## Core Technical Stack

- **Language**: Python 3.10+
- **GUI Framework**: PyQt6 or PySide6 (to be determined based on licensing needs)
- **Video Handling**: `yt-dlp` (maintained fork of youtube-dl) for robust YouTube downloading
- **Data Handling**: SQLite for local storage of download history and preferences
- **Package Manager**: pip with `requirements.txt` for dependency management
- **IDE**: PyCharm (evidenced by .idea/ directory)

## Project Structure

When the project matures, expect this structure:

```
youtube-download/
├── src/
│   ├── core/              # Core download and video handling logic
│   │   ├── downloader.py  # Main yt-dlp wrapper
│   │   ├── manager.py     # Download queue and state management
│   │   └── validators.py  # URL and format validation
│   ├── gui/               # PyQt/PySide UI components
│   │   ├── main_window.py # Main application window
│   │   ├── dialogs/       # Modal dialogs (settings, queue, etc.)
│   │   └── widgets/       # Reusable UI components
│   ├── services/          # Business logic and integrations
│   │   ├── config.py      # Configuration and environment management
│   │   ├── logger.py      # Logging setup
│   │   └── storage.py     # Database and file operations
│   └── utils/             # Utility functions
├── tests/                 # Unit and integration tests
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
└── .github/copilot-instructions.md
```

## Critical Development Patterns

### 1. Download Management with yt-dlp

All YouTube downloading is handled through the `yt-dlp` library. Key patterns:

- **Wrapper Class**: Create a `Downloader` service class that encapsulates `yt-dlp.YoutubeDL` configuration
- **Error Handling**: Network errors, unavailable videos, and format issues are common—wrap yt-dlp calls in try-catch with specific exception handling
- **Format Selection**: yt-dlp uses format codes (e.g., `best[ext=mp4]`). Maintain a `QUALITY_PRESETS` dict mapping user-friendly names to yt-dlp format strings
- **Event Callbacks**: Use progress hooks and logger hooks from yt-dlp to update GUI without blocking the main thread

### 2. GUI Architecture (PyQt6/PySide6)

- **Threading**: Download operations **MUST** run in worker threads using `QThread` to prevent UI freezing
- **Signals/Slots**: Use Qt signals to communicate between worker threads and GUI (never update UI directly from worker threads)
- **Model-View Separation**: Maintain separate models (download queue, history) from view components
- **Settings Dialog**: Use QSettings for persistent configuration (output directory, quality preferences, etc.)

### 3. Configuration Management

All external paths and API-related configs (if any) use environment variables:

```python
import os
from pathlib import Path

DOWNLOADS_DIR = Path(os.getenv("DOWNLOADS_DIR", Path.home() / "Downloads"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
```

**Never** hardcode paths or settings. Store user preferences in SQLite (via settings table or QSettings) and environment variables for deployment.

### 4. State Management

- **Download Queue**: Implement a `DownloadManager` service that tracks active, pending, and completed downloads
- **Signals/Events**: Emit events (status changed, progress, error) so the GUI can react without polling
- **Persistence**: Store completed download metadata and user preferences in SQLite for history and resumability

### 5. Error Handling & Logging

- Use Python's `logging` module (not print statements)
- Create a dedicated `logger.py` that configures handlers (file + console)
- Catch specific exceptions (e.g., `yt_dlp.utils.DownloadError`, network errors) and provide user-friendly messages in the GUI
- Log all download attempts with URL, format, timestamp, and outcome

## Code Quality & Best Practices

### Clean Code Principles

- **Meaningful Names**: Function names should clearly describe intent (e.g., `validate_youtube_url()` not `check_url()`)
- **Single Responsibility**: Each class/module handles one concern (e.g., `Downloader` for yt-dlp interaction, `StorageService` for database)
- **Avoid Magic Values**: Use named constants (`QUALITY_PRESETS`, `TIMEOUT_SECONDS`, etc.)

### Type Hints

- **Mandatory**: Use Python 3.10+ type hints for all functions and class attributes
- Example:

```python
def download_video(self, url: str, quality: str) -> bool:
    """Download a video from YouTube."""
```

### Testing

- **Unit Tests**: Test validators, format selection logic, and error handling in isolation (mock yt-dlp)
- **Integration Tests**: Test the full download flow with real yt-dlp calls (marked as `@pytest.mark.slow`)
- **Test Runner**: Use `pytest` with fixtures for database cleanup between tests
- **No External Dependencies in Tests**: Mock network calls; never hit the actual YouTube in CI/CD

### Code Comments

- **Code is self-documenting**: Avoid comments. Exception: complex algorithm logic or non-obvious workarounds (e.g., yt-dlp version-specific behavior)
- Example of acceptable comment:

```python
# yt-dlp requires raw URLs for age-restricted videos; signature extraction fails otherwise
```

## Workflows & Commands

### Local Development

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux; use .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # for testing and linting

# Run the application
python main.py
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run only fast tests (skip slow integration tests)
pytest -m "not slow"
```

### Code Quality

```bash
# Linting
pylint src/

# Formatting (if using Black)
black --check src/

# Type checking
mypy src/
```

### Building Executables

The project will eventually use PyInstaller to build standalone executables:

```bash
# Build for current platform
pyinstaller --name "YouTube Download" --onefile main.py
```

**Do not** hardcode build scripts; use a Makefile or CI/CD pipeline for cross-platform builds.

## Conventions & Patterns from This Project

### Commit Messages

Follow [Conventional Commits](git-commit-instructions.md):

- Format: `type(scope): subject`
- Scopes for this project: `core`, `gui`, `services`, `tests`, `build`, `ci`, `docs`
- Example: `feat(core): add support for playlist downloads`

### Scope Examples

- `feat(gui): add quality selector dropdown`
- `fix(core): handle age-restricted video URLs`
- `test(services): add unit tests for config validation`
- `refactor(services): extract url validation into separate function`

## Integration Points & Dependencies

### External APIs & Libraries

1. **yt-dlp**: The core library for YouTube interaction
   - Handles URL validation, format extraction, and video download
   - Keep yt-dlp binaries and configuration isolated in `core.downloader`

2. **SQLite**: Local database (built into Python)
   - Stores download history, user preferences, queue state
   - Use a dedicated `StorageService` class for all DB operations

3. **PyQt6/PySide6**: GUI framework
   - Renders main window, dialogs, and progress displays
   - Must not block the event loop during downloads

### Cross-Component Communication

- **GUI → Download Manager**: Signal that user clicked "Download" with URL and quality
- **Download Manager → GUI**: Emit progress signals (bytes downloaded, ETA, status changes)
- **Storage Service ← Download Manager**: Persist download history after completion
- **Config Service ← GUI**: Save user preferences when settings dialog is closed

## Environment & Secrets

- **Local Development**: Create `.env` file (in `.gitignore`) with paths and preferences
- **Example `.env`**:
  ```
  DOWNLOADS_DIR=/Users/username/Downloads
  LOG_LEVEL=DEBUG
  DATABASE_PATH=./app_data/downloads.db
  ```
- **CI/CD**: Environment variables injected by the runner; never commit secrets

## Key Files to Review First

When onboarding:

1. **main.py** – Application entry point and initialization
2. **src/core/downloader.py** – yt-dlp integration (once created)
3. **src/services/config.py** – Configuration and environment handling
4. **src/gui/main_window.py** – Main UI layout and event handling
5. **requirements.txt** – Dependency versions

## AI Agent Guidance

When implementing new features:

1. **Identify the layer**: Is this a core feature (downloader), service (storage), or GUI element?
2. **Add type hints**: Every function must have parameter and return type annotations
3. **Write tests first**: For business logic, write tests before implementation
4. **Handle threading**: Any blocking operation (downloads, file I/O) must use `QThread` or `concurrent.futures`
5. **Log meaningfully**: Include context (URL, format, user action) in log messages
6. **Validate early**: Check user input (URLs, paths) as close to the entry point as possible
7. **Reference existing patterns**: Before inventing a new pattern, check how similar problems are solved in the codebase

---

**Last Updated**: December 28, 2025  
**Project Stage**: Early Development (MVP architecture defined, awaiting implementation)
