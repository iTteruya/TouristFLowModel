import copy
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QMessageBox, QCalendarWidget, QRadioButton, QButtonGroup, QDialog, QDialogButtonBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from datetime import datetime
from dateutil.relativedelta import relativedelta
from config import all_factors_by_category

def generate_dates(start_date, end_date):
    # Determine the format based on the length of the input dates
    if len(start_date) == 10 and len(end_date) == 10:
        format = "%d-%m-%Y"
        increment = relativedelta(days=1)
    elif len(start_date) == 7 and len(end_date) == 7:
        format = "%m-%Y"
        increment = relativedelta(months=1)
    elif len(start_date) == 4 and len(end_date) == 4:
        format = "%Y"
        increment = relativedelta(years=1)
    else:
        print("Некорректный формат даты")
        return []

    # Convert string dates to datetime objects
    start = datetime.strptime(start_date, format)
    end = datetime.strptime(end_date, format)

    # Swap start and end if start is greater than end
    if start > end:
        start, end = end, start

    # Generate dates between start and end using the specified format
    current = start
    dates = []
    while current <= end:
        dates.append(current.strftime(format))
        current += increment

    return dates


class CalendarDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
                                           Qt.Orientation.Horizontal, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.calendar)
        main_layout.addWidget(self.button_box)
        self.setLayout(main_layout)

    def selected_date(self):
        return self.calendar.selectedDate()


class DateSelector(QWidget):

    def __init__(self, app):
        super().__init__()

        self.app = app
        self.selected_date1 = ""
        self.selected_date2 = ""
        self.level_of_detail = None
        self.cur_query = None
        self.init_ui()

    def init_ui(self):
        self.app.init_database()

        layout = QVBoxLayout()

        detail_layout = QHBoxLayout()
        label_detail = QLabel("Степень детализации:")
        label_detail.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        detail_layout.addWidget(label_detail)
        self.detail_group = QButtonGroup(self)

        year_radio = QRadioButton("Год")
        year_radio.setObjectName("-YEAR-")
        year_radio.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        year_radio.clicked.connect(self.set_detail_level)
        self.detail_group.addButton(year_radio)
        detail_layout.addWidget(year_radio)

        month_year_radio = QRadioButton("Месяц-Год")
        month_year_radio.setObjectName("-MONTH_YEAR-")
        month_year_radio.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        month_year_radio.clicked.connect(self.set_detail_level)
        self.detail_group.addButton(month_year_radio)
        detail_layout.addWidget(month_year_radio)

        full_date_radio = QRadioButton("Полная дата")
        full_date_radio.setObjectName("-FULL_DATE-")
        full_date_radio.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        full_date_radio.clicked.connect(self.set_detail_level)
        full_date_radio.setChecked(True)
        self.detail_group.addButton(full_date_radio)
        detail_layout.addWidget(full_date_radio)
        layout.addLayout(detail_layout)

        date1_layout = QHBoxLayout()
        label_date1 = QLabel("Выберите Дату 1:")
        label_date1.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        date1_layout.addWidget(label_date1)
        self.date1_input = QLineEdit()
        self.date1_input.setPlaceholderText("DD-MM-YYYY")
        date1_layout.addWidget(self.date1_input)
        self.calendar1_button = QPushButton("Выбрать Дату 1")
        self.calendar1_button.clicked.connect(self.show_calendar1)
        date1_layout.addWidget(self.calendar1_button)
        layout.addLayout(date1_layout)

        date2_layout = QHBoxLayout()
        label_date2 = QLabel("Выберите Дату 2:")
        label_date2.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        date2_layout.addWidget(label_date2)
        self.date2_input = QLineEdit()
        self.date2_input.setPlaceholderText("DD-MM-YYYY")
        date2_layout.addWidget(self.date2_input)
        self.calendar2_button = QPushButton("Выбрать Дату 2")
        self.calendar2_button.clicked.connect(self.show_calendar2)
        date2_layout.addWidget(self.calendar2_button)
        layout.addLayout(date2_layout)

        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Выбрать Даты")
        self.save_button.clicked.connect(self.save_dates)
        self.save_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        button_layout.addWidget(self.save_button)
        layout.addLayout(button_layout)

        selected_dates_layout1 = QHBoxLayout()
        label_selected_date1 = QLabel("Выбрана Дата 1: ")
        label_selected_date1.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        selected_dates_layout1.addWidget(label_selected_date1)
        self.selected_date1_label = QLabel("")
        self.selected_date1_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        selected_dates_layout1.addWidget(self.selected_date1_label)
        layout.addLayout(selected_dates_layout1)

        selected_dates_layout2 = QHBoxLayout()
        label_selected_date2 = QLabel("Выбрана Дата 2: ")
        label_selected_date2.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        selected_dates_layout2.addWidget(label_selected_date2)
        self.selected_date2_label = QLabel("")
        self.selected_date2_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        selected_dates_layout2.addWidget(self.selected_date2_label)
        layout.addLayout(selected_dates_layout2)

        button_font = QFont()
        button_font.setPointSize(14)  # Set the font size for buttons
        button_font.setBold(True)  # Make the button font bold

        nav_button_layout = QHBoxLayout()
        back_button = QPushButton("Назад")
        back_button.setFont(button_font)
        back_button.clicked.connect(self.go_back)
        nav_button_layout.addWidget(back_button)
        next_button = QPushButton("Далее")
        next_button.setFont(button_font)
        next_button.clicked.connect(self.go_to_next)
        nav_button_layout.addWidget(next_button)
        layout.addLayout(nav_button_layout)

        self.button_home = QPushButton("Меню", self)
        self.button_home.setFont(button_font)
        self.button_home.clicked.connect(self.return_to_main)
        layout.addWidget(self.button_home)

        self.setLayout(layout)
        self.setWindowTitle("Выбор Дат")
        self.setMinimumSize(450, 350)  # Set a minimum size for the window
        self.resize(1280, 720)  # Allow resizing

    def set_detail_level(self):
        radio = self.detail_group.checkedButton()
        if radio:
            self.level_of_detail = radio.objectName()

            if self.level_of_detail == "-FULL_DATE-":
                self.calendar1_button.setEnabled(True)
                self.calendar2_button.setEnabled(True)
                self.calendar1_button.setStyleSheet("")  # reset style
                self.calendar2_button.setStyleSheet("")
                self.date1_input.setEnabled(False)
                self.date2_input.setEnabled(False)
            else:
                self.calendar1_button.setEnabled(False)
                self.calendar2_button.setEnabled(False)
                # Visually grey out using stylesheet
                grey_style = "QPushButton { background-color: lightgray; color: gray; }"
                self.calendar1_button.setStyleSheet(grey_style)
                self.calendar2_button.setStyleSheet(grey_style)
                self.date1_input.setEnabled(True)
                self.date2_input.setEnabled(True)

    def show_calendar1(self):
        dialog = CalendarDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.date1_input.setText(dialog.selected_date().toString("dd-MM-yyyy"))

    def show_calendar2(self):
        dialog = CalendarDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.date2_input.setText(dialog.selected_date().toString("dd-MM-yyyy"))

    def validate_date_range(self, date1, date2):
        format = "%d-%m-%Y" if len(date1) == 10 and len(date2) == 10 else "%m-%Y" if len(date1) == 7 and len(
            date2) == 7 else "%Y"
        year1 = datetime.strptime(date1, format).year
        year2 = datetime.strptime(date2, format).year
        if not (2000 <= year1 <= 2025) or not (2000 <= year2 <= 2025):
            raise InvalidDateError("Выбранные даты должны быть в диапазоне от 2000 до 2026 года")

    def save_dates(self):
        date1 = self.date1_input.text()
        date2 = self.date2_input.text()

        if self.level_of_detail == "-YEAR-":
            format = "%Y"
        elif self.level_of_detail == "-MONTH_YEAR-":
            format = "%m-%Y"
        else:
            format = "%d-%m-%Y"

        try:
            datetime.strptime(date1, format)
            datetime.strptime(date2, format)
            self.validate_date_range(date1, date2)
            self.selected_date1 = date1
            self.selected_date2 = date2
            self.selected_date1_label.setText(date1)
            self.selected_date2_label.setText(date2)
        except ValueError:
            self.show_warning_message("Некорректный формат даты. Пожалуйста введите дату в правильном формате.")
        except InvalidDateError as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def go_back(self):
        self.hide()
        self.app.run_region_selection()

    def return_to_main(self):
        self.hide()
        self.app.run_start_menu()

    def go_to_next(self):

        if self.selected_date1 and self.selected_date2:
            self.app.period = generate_dates(self.selected_date1, self.selected_date2)

            if self.app.skip_eval is True:

                self.app.factors = all_factors_by_category
                self.app.form_query()

                if self.cur_query != self.app.query:
                    if not self.app.use_database and len(self.app.period[0]) == 10:
                        for area, area_data in self.app.query.items():
                            self.app.db.area[area].partial_fulldate(self.app.period)
                    self.cur_query = copy.deepcopy(self.app.query)

                    area_flows = {}
                    for area, area_data in self.cur_query.items():
                        area_flow = []
                        for date, date_data in area_data.items():
                            date_flow = self.app.db.area[area].date[date].tourist_flow
                            area_flow.append(date_flow)
                        area_flows[area] = area_flow

                    flow = [sum(items) for items in zip(*area_flows.values())]

                    self.app.tourist_flow = flow
                    self.app.area_flows = area_flows

                self.app.run_setup_forecast()
            else:
                self.app.run_factor_selector()
            self.hide()
        else:
            self.show_warning_message("Пожалуйста, выберите обе даты.")

    def closeEvent(self, event):
        self.app.close()

    def show_window(self):
        self.show()

    def show_warning_message(self, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Предупреждение")

        # Set message box font and alignment
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        msg_box.setFont(font)

        msg_label = QLabel(message)
        msg_label.setFont(font)
        msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg_box.layout().addWidget(msg_label, 0, 0, 1, msg_box.layout().columnCount(), Qt.AlignmentFlag.AlignCenter)

        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()


class InvalidDateError(Exception):
    pass
