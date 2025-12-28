"""YouTube Download - Main application entry point."""
import sys
from PyQt6.QtWidgets import QApplication

from src.gui.main_window import MainWindow
from src.gui.styles import STYLESHEET
from src.services.logger import app_logger


def main() -> None:
    """Initialize and run the application."""
    app_logger.info("Starting YouTube Download application")

    app = QApplication(sys.argv)
    app.setApplicationName("YouTube Download")
    app.setOrganizationName("YouTube Download")
    app.setStyleSheet(STYLESHEET)

    window = MainWindow()
    window.show()

    app_logger.info("Application window displayed")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
