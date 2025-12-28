"""Style constants for the application."""

# Pastel beige color palette
COLORS = {
    "background": "#F5F5DC",  # Beige
    "background_dark": "#E8E3D3",  # Darker beige
    "primary": "#D4C5B9",  # Warm beige
    "secondary": "#E5D4C1",  # Light beige
    "accent": "#C9B8A8",  # Medium beige
    "text": "#5C4F3D",  # Dark brown
    "text_light": "#8B7D6B",  # Medium brown
    "success": "#B8D4B8",  # Pastel green
    "error": "#E8B4B4",  # Pastel red
    "warning": "#F4D9A6",  # Pastel yellow
    "border": "#D0C4B8",  # Light brown
    "button": "#D4C5B9",  # Warm beige
    "button_hover": "#C9B8A8",  # Medium beige
    "button_pressed": "#B8A898",  # Dark beige
}

# Application stylesheet
STYLESHEET = f"""
QMainWindow {{
    background-color: {COLORS['background']};
}}

QWidget {{
    background-color: {COLORS['background']};
    color: {COLORS['text']};
    font-family: 'Segoe UI', 'San Francisco', 'Helvetica', Arial, sans-serif;
    font-size: 13px;
}}

QLabel {{
    color: {COLORS['text']};
    background-color: transparent;
}}

QLineEdit {{
    background-color: white;
    border: 2px solid {COLORS['border']};
    border-radius: 6px;
    padding: 8px 12px;
    color: {COLORS['text']};
    font-size: 14px;
}}

QLineEdit:focus {{
    border: 2px solid {COLORS['accent']};
}}

QPushButton {{
    background-color: {COLORS['button']};
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    color: {COLORS['text']};
    font-weight: bold;
    font-size: 14px;
}}

QPushButton:hover {{
    background-color: {COLORS['button_hover']};
}}

QPushButton:pressed {{
    background-color: {COLORS['button_pressed']};
}}

QPushButton:disabled {{
    background-color: {COLORS['background_dark']};
    color: {COLORS['text_light']};
}}

QComboBox {{
    background-color: white;
    border: 2px solid {COLORS['border']};
    border-radius: 6px;
    padding: 8px 12px;
    color: {COLORS['text']};
    font-size: 14px;
}}

QComboBox:hover {{
    border: 2px solid {COLORS['accent']};
}}

QComboBox::drop-down {{
    border: none;
    width: 30px;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid {COLORS['text']};
    margin-right: 10px;
}}

QComboBox QAbstractItemView {{
    background-color: white;
    border: 2px solid {COLORS['border']};
    selection-background-color: {COLORS['secondary']};
    selection-color: {COLORS['text']};
    padding: 4px;
}}

QProgressBar {{
    border: 2px solid {COLORS['border']};
    border-radius: 6px;
    background-color: white;
    text-align: center;
    color: {COLORS['text']};
    font-weight: bold;
}}

QProgressBar::chunk {{
    background-color: {COLORS['success']};
    border-radius: 4px;
}}

QListWidget {{
    background-color: white;
    border: 2px solid {COLORS['border']};
    border-radius: 8px;
    padding: 8px;
}}

QListWidget::item {{
    background-color: {COLORS['secondary']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 12px;
    margin: 4px;
}}

QListWidget::item:selected {{
    background-color: {COLORS['accent']};
}}

QListWidget::item:hover {{
    background-color: {COLORS['primary']};
}}

QScrollBar:vertical {{
    background-color: {COLORS['background']};
    width: 14px;
    margin: 0px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS['accent']};
    border-radius: 7px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {COLORS['button_hover']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background-color: {COLORS['background']};
    height: 14px;
    margin: 0px;
}}

QScrollBar::handle:horizontal {{
    background-color: {COLORS['accent']};
    border-radius: 7px;
    min-width: 30px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {COLORS['button_hover']};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}

QGroupBox {{
    border: 2px solid {COLORS['border']};
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 16px;
    font-weight: bold;
    color: {COLORS['text']};
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 4px 12px;
    background-color: {COLORS['background']};
    border-radius: 4px;
}}

QRadioButton {{
    spacing: 8px;
    color: {COLORS['text']};
}}

QRadioButton::indicator {{
    width: 18px;
    height: 18px;
}}

QRadioButton::indicator:unchecked {{
    border: 2px solid {COLORS['border']};
    border-radius: 9px;
    background-color: white;
}}

QRadioButton::indicator:checked {{
    border: 2px solid {COLORS['accent']};
    border-radius: 9px;
    background-color: {COLORS['accent']};
}}

QMessageBox {{
    background-color: {COLORS['background']};
}}

QMessageBox QPushButton {{
    min-width: 80px;
}}
"""
