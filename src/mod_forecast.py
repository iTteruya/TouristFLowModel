from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox, QMessageBox, QScrollArea
)
from config import all_factors_by_category, trans_infr, acc_seg, food_seg, rr, other, num_value

all_factors = [trans_infr, acc_seg, food_seg, rr, other, num_value]
names_of = ["Транспортный сегмент", "Сегмент размещения", "Пищевой сегмент",
            "Сегмент отдыха и развлечений", "Другие факторы", "Количественные факторы"]

parameters = []

for i, section in enumerate(names_of):
    for j, name in enumerate(all_factors[i]):
        parameter = {
            'section': section,
            'name': name,
            'value': None,
            'use_checkbox': False,
            'delta_value': None,
            'options': ['Up', 'Down', 'Mix'],
            'selected_option': 'Up'
        }
        parameters.append(parameter)


class SetupForecast(QMainWindow):

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setMinimumSize(600, 600)  # Minimum size for the window
        self.resize(1280, 720)  # Initial size of the window

        # Central widget with scroll area
        self.central_widget = QWidget()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(self.central_widget)

        self.setCentralWidget(self.scroll_area)

        self.central_layout = QVBoxLayout()
        self.central_widget.setLayout(self.central_layout)

        self.create_ui()

    def create_ui(self):
        self.steps_label = QLabel('Количество шагов:')
        self.steps_label.setFont(QFont('Helvetica', 10))
        self.num_steps_input = QLineEdit()
        self.num_steps_input.setFixedWidth(100)
        self.central_layout.addWidget(self.steps_label)
        self.central_layout.addWidget(self.num_steps_input)

        self.elements_layout = QVBoxLayout()

        self.checkbox_elements = []
        self.input_elements = []
        self.combo_elements = []
        self.delta_input_elements = []

        current_section = None
        for parameter in parameters:
            section = parameter['section']
            name = parameter['name']
            use_checkbox = parameter['use_checkbox']

            if section != current_section:
                current_section = section
                section_label = QLabel(section)
                section_label.setFont(QFont('Helvetica', 12, QFont.Weight.Bold))
                self.elements_layout.addWidget(section_label)

            horizontal_layout = QHBoxLayout()

            checkbox = QCheckBox()
            checkbox.setChecked(use_checkbox)
            checkbox.setObjectName(name)  # Use name as object name to identify later
            checkbox.stateChanged.connect(self.toggle_input)
            horizontal_layout.addWidget(checkbox)
            self.checkbox_elements.append(checkbox)

            name_label = QLabel(f'{name}:')
            name_label.setFont(QFont('Helvetica', 10))
            name_label.setFixedWidth(200)
            name_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)  # Align left and center vertically
            horizontal_layout.addWidget(name_label)

            input_element = QLineEdit()
            input_element.setObjectName(f'value_{name}')
            input_element.setEnabled(use_checkbox)  # Initially enable/disable based on use_checkbox
            input_element.setStyleSheet("background-color: lightgray;" if not use_checkbox else "")
            horizontal_layout.addWidget(input_element)
            self.input_elements.append(input_element)

            delta_label = QLabel('Delta:')
            delta_label.setFixedWidth(40)
            delta_label.setFont(QFont('Helvetica', 10))
            horizontal_layout.addWidget(delta_label)

            delta_input_element = QLineEdit()
            delta_input_element.setObjectName(f'delta_{name}')
            delta_input_element.setEnabled(use_checkbox)  # Initially enable/disable based on use_checkbox
            delta_input_element.setStyleSheet("background-color: lightgray;" if not use_checkbox else "")
            horizontal_layout.addWidget(delta_input_element)
            self.delta_input_elements.append(delta_input_element)

            option_label = QLabel('Option:')
            option_label.setFixedWidth(50)
            option_label.setFont(QFont('Helvetica', 10))
            horizontal_layout.addWidget(option_label)

            combo_element = QComboBox()
            combo_element.addItems(parameter['options'])
            combo_element.setCurrentText(parameter['selected_option'])
            combo_element.setEnabled(use_checkbox)  # Initially enable/disable based on use_checkbox
            combo_element.setObjectName(f'option_{name}')
            combo_element.setStyleSheet("background-color: lightgray;" if not use_checkbox else "")
            horizontal_layout.addWidget(combo_element)
            self.combo_elements.append(combo_element)

            self.elements_layout.addLayout(horizontal_layout)
            self.elements_layout.addSpacing(2)  # Adjusted spacing between rows

        self.central_layout.addLayout(self.elements_layout)
        self.central_layout.addSpacing(10)

        # Check/Uncheck all buttons
        check_all_button = QPushButton('Выбрать все')
        check_all_button.clicked.connect(self.check_all)
        uncheck_all_button = QPushButton('Снять все')
        uncheck_all_button.clicked.connect(self.uncheck_all)
        button_layout = QHBoxLayout()
        button_layout.addWidget(uncheck_all_button)
        button_layout.addWidget(check_all_button)
        self.central_layout.addLayout(button_layout)

        # Navigation buttons
        nav_layout = QHBoxLayout()
        home_button = QPushButton("Меню", self)
        home_button.clicked.connect(self.return_to_main)
        back_button = QPushButton('Назад')
        back_button.clicked.connect(self.go_back)
        next_button = QPushButton('Далее')
        next_button.clicked.connect(self.go_to_next)
        nav_layout.addWidget(home_button)
        nav_layout.addWidget(back_button)
        nav_layout.addWidget(next_button)
        self.central_layout.addLayout(nav_layout)

    def toggle_input(self, checked):
        checkbox = self.sender()
        index = self.checkbox_elements.index(checkbox)

        input_element = self.input_elements[index]
        combo_element = self.combo_elements[index]
        delta_input_element = self.delta_input_elements[index]

        enabled = checked
        input_element.setEnabled(enabled)
        combo_element.setEnabled(enabled)
        delta_input_element.setEnabled(enabled)

        if enabled:
            input_element.setStyleSheet("")
            combo_element.setStyleSheet("")
            delta_input_element.setStyleSheet("")
        else:
            input_element.setStyleSheet("background-color: lightgray;")
            combo_element.setStyleSheet("background-color: lightgray;")
            delta_input_element.setStyleSheet("background-color: lightgray;")

    def check_all(self):
        for checkbox, input_element, combo_element, delta_input_element in zip(
                self.checkbox_elements,
                self.input_elements,
                self.combo_elements,
                self.delta_input_elements
        ):
            checkbox.setChecked(True)
            input_element.setEnabled(True)
            combo_element.setEnabled(True)
            delta_input_element.setEnabled(True)

            input_element.setStyleSheet("")
            combo_element.setStyleSheet("")
            delta_input_element.setStyleSheet("")

    def uncheck_all(self):
        for checkbox, input_element, combo_element, delta_input_element in zip(
                self.checkbox_elements,
                self.input_elements,
                self.combo_elements,
                self.delta_input_elements
        ):
            checkbox.setChecked(False)
            input_element.setEnabled(False)
            combo_element.setEnabled(False)
            delta_input_element.setEnabled(False)

            input_element.setStyleSheet("background-color: lightgray;")
            combo_element.setStyleSheet("background-color: lightgray;")
            delta_input_element.setStyleSheet("background-color: lightgray;")

    def return_to_main(self):
        self.hide()
        self.app.run_start_menu()

    def go_back(self):
        self.hide()

        if self.app.skip_eval is True:
            self.app.run_date_selection()
        else:
            self.app.run_plot_flow()

    def go_to_next(self):
        selected_items = {}
        has_invalid_input = False

        self.app.factors = all_factors_by_category
        self.app.form_query()

        for parameter, checkbox, input_element, combo_element, delta_input_element in zip(
                parameters,
                self.checkbox_elements,
                self.input_elements,
                self.combo_elements,
                self.delta_input_elements
        ):
            name = parameter['name']
            use_checkbox = checkbox.isChecked()

            if use_checkbox:
                value = input_element.text().strip()
                delta_value = delta_input_element.text().strip()
                selected_option = combo_element.currentText()

                try:
                    value = float(value)
                    delta_value = float(delta_value)
                    selected_items[name] = {
                        'section': parameter['section'],
                        'value': value,
                        'delta_value': delta_value,
                        'selected_option': selected_option
                    }
                except ValueError:
                    has_invalid_input = True

        if has_invalid_input:
            QMessageBox.critical(self, 'Ошибка', 'Неверный ввод. Пожалуйста, введите числовые значения для всех выделенных полей.')
            return

        if not selected_items:
            QMessageBox.critical(self, 'Ошибка', 'Пожалуйста, выберите хотя бы один параметр.')
            return

        num_steps = self.num_steps_input.text().strip()
        try:
            num_steps = int(num_steps)
            if num_steps <= 0:
                raise ValueError("Number of steps must be positive")
            self.app.steps = num_steps
        except ValueError:
            QMessageBox.critical(self, 'Ошибка', 'Введите корректное положительное число для количества шагов.')
            return

        self.app.gen_fac = selected_items
        self.hide()
        self.app.run_forecast()

    def show_window(self):
        self.show()

    def closeEvent(self, event):
        self.app.close()