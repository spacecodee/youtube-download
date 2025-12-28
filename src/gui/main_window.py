"""Main application window."""
from typing import Optional

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QCloseEvent
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox,
    QListWidget, QListWidgetItem, QProgressBar,
    QGroupBox, QRadioButton, QMessageBox, QApplication
)

from src.core.downloader import Downloader, DownloadType
from src.core.manager import DownloadManager, DownloadTask, DownloadStatus
from src.core.validators import validate_youtube_url
from src.gui.styles import COLORS
from src.services.logger import app_logger


class DownloadItemWidget(QWidget):
    """Widget for displaying a download item in the list."""

    def __init__(self, task: DownloadTask, parent: Optional[QWidget] = None) -> None:
        """Initialize the download item widget.

        Args:
            task: Download task to display
            parent: Parent widget
        """
        super().__init__(parent)
        self.task = task
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        title_label = QLabel(self.task.title)
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(12)
        title_label.setFont(title_font)
        layout.addWidget(title_label)

        url_label = QLabel(self.task.url)
        url_label.setStyleSheet(f"color: {COLORS['text_light']}; font-size: 11px;")
        url_label.setWordWrap(True)
        layout.addWidget(url_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(int(self.task.progress))
        layout.addWidget(self.progress_bar)

        info_layout = QHBoxLayout()
        self.status_label = QLabel(self._get_status_text())
        self.status_label.setStyleSheet(f"color: {self._get_status_color()};")
        info_layout.addWidget(self.status_label)
        info_layout.addStretch()

        quality_label = QLabel(f"Calidad: {self.task.quality}")
        quality_label.setStyleSheet(f"color: {COLORS['text_light']};")
        info_layout.addWidget(quality_label)

        layout.addLayout(info_layout)

    def update_progress(self, progress: float) -> None:
        """Update the progress bar.

        Args:
            progress: Progress percentage
        """
        self.progress_bar.setValue(int(progress))

    def update_status(self, status: DownloadStatus) -> None:
        """Update the status label.

        Args:
            status: New status
        """
        self.task.status = status
        self.status_label.setText(self._get_status_text())
        self.status_label.setStyleSheet(f"color: {self._get_status_color()};")

    def _get_status_text(self) -> str:
        """Get status text in Spanish."""
        status_map = {
            DownloadStatus.PENDING: "Pendiente",
            DownloadStatus.DOWNLOADING: "Descargando...",
            DownloadStatus.COMPLETED: "Completado",
            DownloadStatus.FAILED: "Error",
            DownloadStatus.CANCELLED: "Cancelado",
        }
        return status_map.get(self.task.status, "Desconocido")

    def _get_status_color(self) -> str:
        """Get color for status."""
        color_map = {
            DownloadStatus.PENDING: COLORS['text_light'],
            DownloadStatus.DOWNLOADING: COLORS['accent'],
            DownloadStatus.COMPLETED: COLORS['success'],
            DownloadStatus.FAILED: COLORS['error'],
            DownloadStatus.CANCELLED: COLORS['warning'],
        }
        return color_map.get(self.task.status, COLORS['text'])


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self) -> None:
        """Initialize the main window."""
        super().__init__()
        self.downloader = Downloader(logger=app_logger)
        self.download_manager = DownloadManager(
            downloader=self.downloader,
            logger=app_logger,
            parent=self
        )

        self.download_widgets: dict[str, tuple[QListWidgetItem, DownloadItemWidget]] = {}

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        self.setWindowTitle("YouTube Download - Descarga música y videos")
        self.setMinimumSize(900, 700)
        self.resize(1000, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        title_label = QLabel("🎵 YouTube Download 🎬")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(f"color: {COLORS['text']}; padding: 10px;")
        main_layout.addWidget(title_label)

        input_group = QGroupBox("Nueva Descarga")
        input_layout = QVBoxLayout(input_group)
        input_layout.setSpacing(12)

        url_layout = QHBoxLayout()
        url_label = QLabel("URL:")
        url_label.setMinimumWidth(80)
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Pega aquí la URL de YouTube o YouTube Music...")
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        input_layout.addLayout(url_layout)

        type_layout = QHBoxLayout()
        type_label = QLabel("Tipo:")
        type_label.setMinimumWidth(80)
        self.video_radio = QRadioButton("Video")
        self.video_radio.setChecked(True)
        self.audio_radio = QRadioButton("Solo Audio (MP3)")
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.video_radio)
        type_layout.addWidget(self.audio_radio)
        type_layout.addStretch()
        input_layout.addLayout(type_layout)

        quality_layout = QHBoxLayout()
        quality_label = QLabel("Calidad:")
        quality_label.setMinimumWidth(80)
        self.quality_combo = QComboBox()
        self.quality_combo.addItems([
            "Mejor calidad",
            "Alta (1080p)",
            "Media (720p)",
            "Baja (480p)",
            "Audio mejor calidad",
            "Audio MP3"
        ])
        quality_layout.addWidget(quality_label)
        quality_layout.addWidget(self.quality_combo)
        input_layout.addLayout(quality_layout)

        button_layout = QHBoxLayout()
        self.download_button = QPushButton("⬇ Descargar")
        self.download_button.setMinimumHeight(40)
        self.download_button.clicked.connect(self._on_download_clicked)
        button_layout.addStretch()
        button_layout.addWidget(self.download_button)
        button_layout.addStretch()
        input_layout.addLayout(button_layout)

        main_layout.addWidget(input_group)

        queue_group = QGroupBox("Cola de Descargas")
        queue_layout = QVBoxLayout(queue_group)

        self.download_list = QListWidget()
        self.download_list.setMinimumHeight(300)
        queue_layout.addWidget(self.download_list)

        main_layout.addWidget(queue_group)

        status_label = QLabel(
            "Arrastra enlaces de YouTube o YouTube Music, incluyendo listas de reproducción"
        )
        status_label.setStyleSheet(
            f"color: {COLORS['text_light']}; padding: 8px; text-align: center;"
        )
        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(status_label)

    def _connect_signals(self) -> None:
        """Connect signals and slots."""
        self.download_manager.download_added.connect(self._on_download_added)
        self.download_manager.download_progress.connect(self._on_download_progress)
        self.download_manager.download_completed.connect(self._on_download_completed)
        self.download_manager.status_changed.connect(self._on_status_changed)

        self.video_radio.toggled.connect(self._on_type_changed)

    def _on_type_changed(self) -> None:
        """Handle download type radio button changes."""
        if self.audio_radio.isChecked():
            self.quality_combo.setCurrentText("Audio mejor calidad")
        else:
            self.quality_combo.setCurrentText("Mejor calidad")

    def _on_download_clicked(self) -> None:
        """Handle download button click."""
        url = self.url_input.text().strip()

        if not url:
            QMessageBox.warning(
                self,
                "URL Vacía",
                "Por favor ingresa una URL de YouTube o YouTube Music."
            )
            return

        is_valid, error_msg = validate_youtube_url(url)
        if not is_valid:
            QMessageBox.warning(self, "URL Inválida", error_msg)
            return

        quality = self.quality_combo.currentText()
        download_type = (
            DownloadType.AUDIO if self.audio_radio.isChecked() else DownloadType.VIDEO
        )

        self.download_button.setEnabled(False)
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        try:
            info = self.downloader.get_video_info(url)
            if info:
                title = info.get("title", "Unknown")
                if "entries" in info:
                    title = info.get("title", "Playlist") + f" ({len(info['entries'])} videos)"
            else:
                title = "Unknown"

            self.download_manager.add_download(url, quality, download_type, title)
            self.url_input.clear()

        except Exception as e:
            app_logger.error(f"Error getting video info: {str(e)}")
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo obtener información del video: {str(e)}"
            )
        finally:
            QApplication.restoreOverrideCursor()
            self.download_button.setEnabled(True)

    def _on_download_added(self, task: DownloadTask) -> None:
        """Handle download added to queue.

        Args:
            task: Download task that was added
        """
        item = QListWidgetItem(self.download_list)
        widget = DownloadItemWidget(task)

        item.setSizeHint(QSize(0, 140))
        self.download_list.addItem(item)
        self.download_list.setItemWidget(item, widget)

        self.download_widgets[task.url] = (item, widget)

    def _on_download_progress(self, url: str, progress: float) -> None:
        """Handle download progress update.

        Args:
            url: Download URL
            progress: Progress percentage
        """
        if url in self.download_widgets:
            _, widget = self.download_widgets[url]
            widget.update_progress(progress)

    def _on_download_completed(self, success: bool, error: str) -> None:
        """Handle download completion.

        Args:
            success: Whether download succeeded
            error: Error message if failed
        """
        if not success and error:
            QMessageBox.critical(
                self,
                "Error de Descarga",
                f"Error al descargar:\n{error}"
            )

    def _on_status_changed(self, url: str, status: DownloadStatus) -> None:
        """Handle download status change.

        Args:
            url: Download URL
            status: New status
        """
        if url in self.download_widgets:
            _, widget = self.download_widgets[url]
            widget.update_status(status)

    def closeEvent(self, a0: Optional[QCloseEvent]) -> None:
        """Handle window close event."""
        if not a0:
            return

        active_downloads = self.download_manager.get_active_downloads()
        if active_downloads:
            reply = QMessageBox.question(
                self,
                "Descargas Activas",
                f"Hay {len(active_downloads)} descarga(s) en progreso.\n"
                "¿Seguro que quieres salir?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.No:
                a0.ignore()
                return

        a0.accept()
