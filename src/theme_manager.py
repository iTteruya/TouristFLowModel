class ThemeManager():

    def __init__(self, app):
        super().__init__()

        self.app = app

    def set_theme(self, theme_style):
        match theme_style:
            case "light": self.set_light_theme()
            case "dark": self.set_dark_theme()
            case _: self.set_light_theme()


    def set_light_theme(self):
        light_stylesheet = """
        QCalendarWidget QWidget#qt_calendar_navigationbar {
            background-color: #F5F5F5;
            color: #2C3E50;
        }
        QCalendarWidget QToolButton {
            color: #2C3E50;
            font-size: 14px;
        }
        QCalendarWidget QAbstractItemView {
            color: #2C3E50;
            background-color: #FFFFFF;
            selection-background-color: #D0E6F6;
            selection-color: #2C3E50;
        }
        QWidget {
            background-color: #FFFFFF;
            color: #2C3E50;
        }
        QPushButton {
            background-color: #E8F1FA;
            border: 1px solid #AFCDE7;
            border-radius: 4px;
            padding: 6px 10px;
            font-size: 14px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #D0E6F6;
        }
        QLineEdit, QTextEdit, QComboBox {
            background-color: #FFFFFF;
            border: 1px solid #AFCDE7;
            border-radius: 3px;
            padding: 4px;
        }
        QListWidget {
            background-color: #FFFFFF;
            border: 1px solid #AFCDE7;
        }
        QListWidget::item:selected {
            background-color: #D0E6F6;
            color: #2C3E50;
        }
        QLabel {
        }
        QRadioButton {
            color: #2C3E50;
        }
        QRadioButton::indicator {
            border: 1px solid #2C3E50;
            background-color: #FFFFFF;
            border-radius: 10px;
            width: 16px;
            height: 16px;
        }
        QRadioButton::indicator:checked {
            background-color: #2C3E50;
        }
        QCheckBox {
            color: #2C3E50;
            spacing: 6px;
        }
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            border: 1px solid #2C3E50;
            background-color: #FFFFFF;
            border-radius: 4px;
        }
        QCheckBox::indicator:checked {
            background-color: #2C3E50;
        }
        QScrollBar:vertical {
            border: none;
            background: #E8F1FA;
            width: 12px;
            margin: 0px;
        }
        QScrollBar::handle:vertical {
            background: #AFCDE7;
            min-height: 20px;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical:hover {
            background: #88B3D1;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
            background: none;
            border: none;
        }
        
        QScrollBar:horizontal {
            border: none;
            background: #E8F1FA;
            height: 12px;
            margin: 0px;
        }
        QScrollBar::handle:horizontal {
            background: #AFCDE7;
            min-width: 20px;
            border-radius: 6px;
        }
        QScrollBar::handle:horizontal:hover {
            background: #88B3D1;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            width: 0px;
            background: none;
            border: none;
        }
        """
        self.app.setStyleSheet(light_stylesheet)

    def set_dark_theme(self):
        dark_stylesheet = """
        QWidget {
            background-color: #2E2E2E;
            color: #F0F0F0;
        }
        QPushButton {
            background-color: #3A3A3A;
            border: 1px solid #F0F0F0;
            padding: 5px;
            font-weight: bold;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #505050;
        }
        QLineEdit {
            background-color: #3A3A3A;
            border: 1px solid #F0F0F0;
            padding: 5px;
        }
        QListWidget {
            background-color: #3A3A3A;
            border: 1px solid #F0F0F0;
        }
        QListWidget::item {
            color: #F0F0F0;
        }
        QListWidget::item:selected {
            background-color: #F0F0F0;
            color: #2E2E2E;
        }
        QRadioButton { color: #ffffff; } 
        QRadioButton::indicator { width: 16px; height: 16px; }
        QCalendarWidget QWidget#qt_calendar_navigationbar {
            background-color: #2b2b2b;
            color: #ffffff;
            border: none;
        }
        QCalendarWidget QToolButton {
            color: #ffffff;
            font-size: 14px;
        }
        QCalendarWidget QToolButton::hover {
            background-color: #ffffff;
        }
        QCalendarWidget QAbstractItemView {
            color: #000000;
            background-color: #ffffff;
            selection-background-color: #ffffff; /* Orange highlight for selected date */
            selection-color: #ffffff;
            border: none;
        }
        QRadioButton::indicator {
            border: 1px solid #000000;  /* Border color */
            border-radius: 10px;  /* Make the indicator circle */
        }
        QRadioButton::indicator:checked {
            background-color: #ffffff;  /* Indicator color when checked */
            border: 1px solid #000000;  /* Border color */
            border-radius: 10px;  /* Ensure circle shape */
        }
        """
        self.app.setStyleSheet(dark_stylesheet)