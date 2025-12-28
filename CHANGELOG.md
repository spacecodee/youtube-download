# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.0.0] - 2025-12-28

### Added

#### Core Features

- ✨ Complete video and audio download system from YouTube using yt-dlp
- ✨ YouTube Music support
- ✨ Full playlist download support
- ✨ Queue management with up to 3 simultaneous downloads
- ✨ YouTube URL validation and automatic playlist detection

#### Graphical Interface

- 🎨 Modern graphical interface with PyQt6
- 🎨 Pastel beige color theme (#F5F5DC, #D4C5B9, #E5D4C1)
- 🎨 Real-time progress bar for each download
- 🎨 Visual states: Pending, Downloading, Completed, Failed, Cancelled
- 🎨 Custom widget for each download item
- 🎨 Warning when closing with active downloads

#### Quality Options

- 📊 Videos: Best quality, High (1080p), Medium (720p), Low (480p)
- 📊 Audio: Best quality, MP3 (192 kbps)
- 📊 Automatic MP3 conversion with FFmpeg

#### System

- 🔧 Configuration system with environment variables (.env)
- 🔧 Complete logging system with log files
- 🔧 Modular project structure (core, gui, services, utils)
- 🔧 Thread management for non-blocking downloads

#### Utilities

- 🛠️ Formatting functions (bytes, speed, time)
- 🛠️ Filename sanitization
- 🛠️ System verification script (start.py)
- 🛠️ Functional test suite (test_functionality.py)

#### Documentation

- 📖 Complete README with installation and usage guide
- 📖 Conventional commit instructions
- 📖 Copilot instructions
- 📖 Configuration examples (.env.example)

### Technical

#### Architecture

```
src/
├── core/              # Business logic
│   ├── downloader.py  # yt-dlp wrapper
│   ├── manager.py     # Download queue management
│   └── validators.py  # URL validation
├── gui/               # Graphical interface
│   ├── main_window.py # Main window
│   └── styles.py      # Styles and colors
├── services/          # Services
│   ├── config.py      # Configuration
│   └── logger.py      # Logging system
└── utils/             # Utilities
    └── helpers.py     # Helper functions
```

#### Dependencies

- PyQt6 6.8.0 - GUI framework
- yt-dlp 2024.12.23+ - Video downloader
- python-dotenv 1.0.1 - Environment variables management
- FFmpeg (external) - Audio/video conversion

#### Requirements

- Python 3.10+
- FFmpeg installed on the system
- Internet connection

### Technical Features

#### Download Management

- Threading with QThread for non-blocking downloads
- Qt signals/slots system for inter-thread communication
- Automatic queue with concurrent download limit
- Robust error and exception handling

#### Validation

- URL validation with regular expressions
- Automatic playlist detection
- Dependency verification on startup

#### Logging

- Console and file logging
- Configurable levels (DEBUG, INFO, WARNING, ERROR)
- Consistent format with timestamps
- Automatic log rotation

#### Configuration

- Environment variables with .env
- Safe default values
- Automatic creation of required directories
- Persistent configuration with QSettings (future)

### Testing

- Complete functional test suite
- Import verification
- Validator tests
- Helper tests
- Configuration tests
- Downloader initialization tests

### Upcoming Features (Roadmap)

#### v1.1.0

- [ ] Download history with SQLite database
- [ ] Pause/resume downloads
- [ ] Destination folder selector per download
- [ ] Video preview before downloading
- [ ] Estimated size information

#### v1.2.0

- [ ] Customizable themes
- [ ] Dark mode
- [ ] Advanced settings in GUI
- [ ] Usage statistics
- [ ] Export/import configuration

#### v1.3.0

- [ ] Subtitle downloads
- [ ] Conversion to different formats
- [ ] Cloud service integration
- [ ] Desktop notifications
- [ ] Customizable keyboard shortcuts

#### v2.0.0

- [ ] Support for other services (Vimeo, Dailymotion, etc.)
- [ ] Complete channel downloads
- [ ] Download scheduler
- [ ] REST API for automation
- [ ] Plugin system

### Known Issues

- ⚠️ FFmpeg required for audio conversion
- ⚠️ Some videos with geographic restrictions may not work
- ⚠️ Private or deleted videos generate errors

### Security

- ✅ No credential storage
- ✅ No unsolicited connections
- ✅ Logs don't contain sensitive information
- ✅ User input validation

---

## Versioning Format

- **MAJOR**: Incompatible API changes
- **MINOR**: New backwards-compatible functionality
- **PATCH**: Backwards-compatible bug fixes

## Types of Changes

- **Added**: for new features
- **Changed**: for changes in existing functionality
- **Deprecated**: for features that will be removed
- **Removed**: for removed features
- **Fixed**: for bug fixes
- **Security**: in case of vulnerabilities
