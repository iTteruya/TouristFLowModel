import sys
import os
import ctypes
from config import ASSETS_DIR
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from theme_manager import ThemeManager
from tourism_app import TourismApp

if __name__ == "__main__":
    appid = u'tourismapp.1.0.0'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)

    app = QApplication(sys.argv)

    icon_path = os.path.join(ASSETS_DIR, "icon.png")
    app.setWindowIcon(QIcon(icon_path))

    theme_manager = ThemeManager(app)
    theme_manager.set_theme("light")

    tourism_app = TourismApp(use_real_data=False, use_llm_analyzer=True)
    tourism_app.set_window_titles()
    tourism_app.run()

    sys.exit(app.exec())
