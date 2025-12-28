"""Download queue and state management."""
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from PyQt6.QtCore import QObject, QThread, pyqtSignal

from src.core.downloader import Downloader, DownloadType


class DownloadStatus(Enum):
    """Status of a download."""
    PENDING = "pending"
    DOWNLOADING = "downloading"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class DownloadTask:
    """Represents a download task."""
    url: str
    quality: str
    download_type: DownloadType
    title: str = "Unknown"
    status: DownloadStatus = DownloadStatus.PENDING
    progress: float = 0.0
    error_message: str = ""


class DownloadWorker(QThread):
    """Worker thread for downloading videos."""

    progress_updated = pyqtSignal(str, float, dict)
    download_completed = pyqtSignal(str, bool, str)

    def __init__(
            self,
            task: DownloadTask,
            downloader: Downloader,
            parent: Optional[QObject] = None
    ) -> None:
        """Initialize the download worker.

        Args:
            task: Download task to execute
            downloader: Downloader instance
            parent: Parent QObject
        """
        super().__init__(parent)
        self.task = task
        self.downloader = downloader
        self._is_cancelled = False

    def run(self) -> None:
        """Execute the download in a worker thread."""
        if self._is_cancelled:
            self.download_completed.emit(self.task.url, False, "Cancelled")
            return

        def progress_callback(d: Dict[str, Any]) -> None:
            if self._is_cancelled:
                return

            if d.get("status") == "downloading":
                downloaded = d.get("downloaded_bytes", 0)
                total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
                if total > 0:
                    progress = (downloaded / total) * 100
                    self.progress_updated.emit(self.task.url, progress, d)

        def error_callback(error: str) -> None:
            self.download_completed.emit(self.task.url, False, error)

        success = self.downloader.download(
            url=self.task.url,
            quality=self.task.quality,
            download_type=self.task.download_type,
            progress_callback=progress_callback,
            error_callback=error_callback
        )

        if not self._is_cancelled:
            self.download_completed.emit(
                self.task.url,
                success,
                "" if success else "Download failed"
            )

    def cancel(self) -> None:
        """Cancel the download."""
        self._is_cancelled = True


class DownloadManager(QObject):
    """Manages download queue and worker threads."""

    download_added = pyqtSignal(DownloadTask)
    download_started = pyqtSignal(str)
    download_progress = pyqtSignal(str, float)
    download_completed = pyqtSignal(str, bool, str)
    status_changed = pyqtSignal(str, DownloadStatus)

    def __init__(
            self,
            downloader: Downloader,
            max_concurrent: int = 3,
            logger: Optional[logging.Logger] = None,
            parent: Optional[QObject] = None
    ) -> None:
        """Initialize the download manager.

        Args:
            downloader: Downloader instance
            max_concurrent: Maximum concurrent downloads
            logger: Logger instance
            parent: Parent QObject
        """
        super().__init__(parent)
        self.downloader = downloader
        self.max_concurrent = max_concurrent
        self.logger = logger or logging.getLogger(__name__)

        self.tasks: Dict[str, DownloadTask] = {}
        self.workers: Dict[str, DownloadWorker] = {}
        self.queue: List[str] = []

    def add_download(
            self,
            url: str,
            quality: str,
            download_type: DownloadType,
            title: str = "Unknown"
    ) -> None:
        """Add a download to the queue.

        Args:
            url: YouTube URL
            quality: Quality preset
            download_type: Type of download
            title: Video title
        """
        if url in self.tasks:
            self.logger.warning(f"Download already exists: {url}")
            return

        task = DownloadTask(
            url=url,
            quality=quality,
            download_type=download_type,
            title=title
        )

        self.tasks[url] = task
        self.queue.append(url)
        self.download_added.emit(task)
        self.logger.info(f"Added download: {title} ({url})")

        self._process_queue()

    def _process_queue(self) -> None:
        """Process the download queue."""
        active_workers = sum(
            1 for worker in self.workers.values() if worker.isRunning()
        )

        while active_workers < self.max_concurrent and self.queue:
            url = self.queue.pop(0)
            task = self.tasks[url]

            if task.status != DownloadStatus.PENDING:
                continue

            self._start_download(task)
            active_workers += 1

    def _start_download(self, task: DownloadTask) -> None:
        """Start downloading a task.

        Args:
            task: Download task to start
        """
        task.status = DownloadStatus.DOWNLOADING
        self.status_changed.emit(task.url, DownloadStatus.DOWNLOADING)
        self.download_started.emit(task.url)

        worker = DownloadWorker(task, self.downloader)
        worker.progress_updated.connect(self._on_progress_updated)
        worker.download_completed.connect(self._on_download_completed)
        worker.finished.connect(lambda: self._on_worker_finished(task.url))

        self.workers[task.url] = worker
        worker.start()

        self.logger.info(f"Started download: {task.title}")

    def _on_progress_updated(self, url: str, progress: float) -> None:
        """Handle progress updates from worker.

        Args:
            url: Download URL
            progress: Progress percentage
        """
        if url in self.tasks:
            self.tasks[url].progress = progress
            self.download_progress.emit(url, progress)

    def _on_download_completed(self, url: str, success: bool, error: str) -> None:
        """Handle download completion from worker.

        Args:
            url: Download URL
            success: Whether download succeeded
            error: Error message if failed
        """
        if url not in self.tasks:
            return

        task = self.tasks[url]

        if success:
            task.status = DownloadStatus.COMPLETED
            task.progress = 100.0
            self.logger.info(f"Completed download: {task.title}")
        else:
            task.status = DownloadStatus.FAILED
            task.error_message = error
            self.logger.error(f"Failed download: {task.title} - {error}")

        self.status_changed.emit(url, task.status)
        self.download_completed.emit(url, success, error)

    def _on_worker_finished(self, url: str) -> None:
        """Handle worker thread finishing.

        Args:
            url: Download URL
        """
        if url in self.workers:
            del self.workers[url]

        self._process_queue()

    def cancel_download(self, url: str) -> None:
        """Cancel a download.

        Args:
            url: Download URL to cancel
        """
        if url in self.workers:
            self.workers[url].cancel()
            self.workers[url].wait()

        if url in self.tasks:
            self.tasks[url].status = DownloadStatus.CANCELLED
            self.status_changed.emit(url, DownloadStatus.CANCELLED)
            self.logger.info(f"Cancelled download: {url}")

        if url in self.queue:
            self.queue.remove(url)

    def get_active_downloads(self) -> List[DownloadTask]:
        """Get all active downloads.

        Returns:
            List of active download tasks
        """
        return [
            task for task in self.tasks.values()
            if task.status == DownloadStatus.DOWNLOADING
        ]

    def get_all_downloads(self) -> List[DownloadTask]:
        """Get all downloads.

        Returns:
            List of all download tasks
        """
        return list(self.tasks.values())
