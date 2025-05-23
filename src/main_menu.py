import os
from config import ASSETS_DIR
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QApplication, QHBoxLayout
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt

class StartScreen(QWidget):

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # App logo
        logo_label = QLabel()
        logo_path = os.path.join(ASSETS_DIR, "logo.png")
        pixmap = QPixmap(logo_path).scaled(
            650, 800,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)

        button_layout = QHBoxLayout()

        eval_button = QPushButton('Оценка потребительской ценности')
        eval_button.clicked.connect(self.start_eval)
        button_layout.addWidget(eval_button)

        forecast_button = QPushButton('Прогноз будущего потока')
        forecast_button.clicked.connect(self.start_forecast)
        button_layout.addWidget(forecast_button)

        layout.addLayout(button_layout)

        exit_button = QPushButton('Выход')
        exit_button.clicked.connect(self.exit_app)
        layout.addWidget(exit_button)

        self.setLayout(layout)
        self.setMinimumSize(450, 350)  # Set a minimum size for the window
        self.resize(1280, 720)  # Allow resizing

    def show_window(self):
        self.show()

    def start_eval(self):
        self.app.skip_eval = False
        self.hide()
        self.app.run_region_selection()

    def start_forecast(self):
        self.app.skip_eval = True
        self.hide()
        self.app.run_region_selection()

    def exit_app(self):
        QApplication.quit()

    def closeEvent(self, event):
        self.app.close()