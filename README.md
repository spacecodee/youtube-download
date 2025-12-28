# YouTube Download 🎵🎬

Cross-platform desktop application for downloading music and videos from YouTube and YouTube Music, with support for
playlists.

## Features

✨ **Download Videos and Audio**

- Videos in multiple qualities (1080p, 720p, 480p)
- Automatic MP3 conversion for audio
- Best quality available automatically

🎨 **Modern Interface**

- Pastel beige color scheme design
- Intuitive and easy-to-use interface
- Real-time progress bar

📋 **Download Management**

- Automatic download queue
- Up to 3 simultaneous downloads
- Full playlist support
- Visual status for each download

## Requirements

- Python 3.10 or higher
- FFmpeg (for audio conversion)

### Installing FFmpeg

**macOS (with Homebrew):**

```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

## Installation

1. **Clone the repository:**

```bash
git clone <repository-url>
cd youtube-download
```

2. **Create virtual environment:**

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Configure (optional):**

```bash
cp .env.example .env
# Edit .env to customize paths and settings
```

## Usage

### Run the application:

```bash
python main.py
```

### Download a video or song:

1. **Paste the URL** from YouTube or YouTube Music in the text field
2. **Select the type**:
    - Video: download the complete video
    - Audio Only (MP3): extract only the audio in MP3 format
3. **Choose the quality** you prefer
4. **Click "Download"**
5. **Watch the progress** in the download queue

### Supported URLs:

- Individual videos: `https://www.youtube.com/watch?v=...`
- Short videos: `https://youtu.be/...`
- Playlists: `https://www.youtube.com/playlist?list=...`
- YouTube Music: `https://music.youtube.com/watch?v=...`

## Project Structure

```
youtube-download/
├── src/
│   ├── core/              # Core download logic
│   │   ├── downloader.py  # yt-dlp wrapper
│   │   ├── manager.py     # Queue management
│   │   └── validators.py  # URL validation
│   ├── gui/               # Graphical interface
│   │   ├── main_window.py # Main window
│   │   └── styles.py      # Styles and colors
│   ├── services/          # Services
│   │   ├── config.py      # Configuration
│   │   └── logger.py      # Logging system
│   └── utils/             # Utilities
│       └── helpers.py     # Helper functions
├── tests/                 # Tests (future)
├── main.py               # Entry point
└── requirements.txt      # Dependencies
```

## Advanced Configuration

Edit the `.env` file to customize:

```env
# Download directory (default: ~/Downloads/YouTube)
DOWNLOADS_DIR=/path/to/your/folder

# Log level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# Local database (for history)
DATABASE_PATH=./app_data/downloads.db

# Maximum simultaneous downloads
MAX_CONCURRENT_DOWNLOADS=3
```

## Quality Options

### Videos:

- **Best quality**: Maximum available quality
- **High (1080p)**: Full HD
- **Medium (720p)**: HD
- **Low (480p)**: SD

### Audio:

- **Best audio quality**: Maximum audio quality
- **MP3 Audio**: Optimized MP3 (192 kbps)

## Troubleshooting

### Error: "FFmpeg not found"

Install FFmpeg following the instructions in the requirements section.

### Error: "Invalid URL"

Make sure the URL is from YouTube or YouTube Music.

### Slow downloads

- Check your internet connection
- Reduce the number of simultaneous downloads in `.env`

### Video not available

Some videos may have geographic or age restrictions.

## Development

### Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

### Run tests:

```bash
pytest
pytest --cov=src  # with coverage
```

### Linting and formatting:

```bash
pylint src/
black src/
mypy src/
```

## Technologies

- **PyQt6**: GUI framework
- **yt-dlp**: Video download library
- **FFmpeg**: Audio/video processing
- **Python 3.10+**: Programming language

## License

This project is open source. See the LICENSE file for more details.

## Contributing

Contributions are welcome. Please:

1. Fork the project
2. Create a branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Follow commit conventions in `.github/git-commit-instructions.md`

## Support

To report bugs or request features, open an issue on GitHub.

## Author

Developed with ❤️ by Spacecodee

---

**Note**: This application is designed for personal use. Respect copyrights and YouTube's terms of service.
