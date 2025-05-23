import pandas as pd
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QListWidget, QPushButton, QLabel, QMessageBox, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class RegionSelector(QWidget):

    def __init__(self, app):
        super().__init__()

        self.app = app

        df = pd.read_csv('../data/areas.csv', encoding='windows-1251')
        self.area_list = df['area'].tolist()
        self.selected_areas = set()
        self.sec_scr_trigger = False
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Выберите регионы", self)
        font = QFont()
        font.setPointSize(16)  # Set the font size
        font.setBold(True)  # Make the font bold
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("Search...")
        layout.addWidget(self.search_box)

        self.list_widget = QListWidget(self)
        self.list_widget.addItems(self.area_list)
        self.list_widget.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.list_widget.itemClicked.connect(self.toggle_selection)

        # Set font for list items
        item_font = QFont()
        item_font.setPointSize(12)  # Set the font size for list items
        item_font.setBold(True)  # Make the list item font bold
        self.list_widget.setFont(item_font)

        layout.addWidget(self.list_widget)

        # Add a compact list to show selected regions
        self.selected_label = QLabel("Выбранные регионы:")
        selected_font = QFont()
        selected_font.setPointSize(12)
        selected_font.setBold(True)
        self.selected_label.setFont(selected_font)
        layout.addWidget(self.selected_label)

        self.selected_list_widget = QListWidget(self)
        self.selected_list_widget.setMaximumHeight(100)  # Compact height
        self.selected_list_widget.setFont(QFont("", 10))  # Smaller font
        layout.addWidget(self.selected_list_widget)

        button_font = QFont()
        button_font.setPointSize(14)  # Set the font size for buttons
        button_font.setBold(True)  # Make the button font bold

        # First row of buttons
        button_row1 = QHBoxLayout()
        self.button_clear = QPushButton("Очистить", self)
        self.button_clear.setFont(button_font)
        button_row1.addWidget(self.button_clear)

        self.button_select = QPushButton("Выбрать", self)
        self.button_select.setFont(button_font)
        button_row1.addWidget(self.button_select)
        layout.addLayout(button_row1)

        # First row of buttons
        button_row2 = QHBoxLayout()
        self.button_home = QPushButton("Меню", self)
        self.button_home.setFont(button_font)
        button_row2.addWidget(self.button_home)

        self.button_next = QPushButton("Далее", self)
        self.button_next.setFont(button_font)
        button_row2.addWidget(self.button_next)
        layout.addLayout(button_row2)

        self.setLayout(layout)
        self.setMinimumSize(450, 350)  # Set a minimum size for the window
        self.resize(1280, 720)  # Allow resizing

        self.search_box.textChanged.connect(self.update_list)
        self.button_select.clicked.connect(self.select_areas)
        self.button_clear.clicked.connect(self.clear_selection)
        self.button_next.clicked.connect(self.go_to_next)
        self.button_home.clicked.connect(self.return_to_main)

    def show_window(self):
        self.show()

    def update_list(self):
        search_term = self.search_box.text().strip().lower()
        self.list_widget.clear()
        filtered_areas = [area for area in self.area_list if search_term in area.lower()]
        self.list_widget.addItems(filtered_areas)
        self.update_selection()

    def toggle_selection(self, item):
        area = item.text()
        if area in self.selected_areas:
            self.selected_areas.remove(area)
        else:
            self.selected_areas.add(area)

        self.update_selection()

    def update_selection(self):
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            if item.text() in self.selected_areas:
                item.setSelected(True)
            else:
                item.setSelected(False)

    def select_areas(self):
        self.selected_list_widget.clear()
        self.selected_list_widget.addItems(sorted(self.selected_areas))
        if self.selected_areas:
            self.sec_scr_trigger = True

    def clear_selection(self):
        self.selected_areas.clear()
        self.sec_scr_trigger = False
        self.update_selection()
        self.selected_list_widget.clear()

    def go_to_next(self):
        if self.sec_scr_trigger:
            self.app.areas = self.selected_areas
            self.hide()
            self.app.run_date_selection()
        else:
            self.show_popup("Предупреждение", "Пожалуйста, выберите хотя бы 1 регион")

    def return_to_main(self):
        self.hide()
        self.app.run_start_menu()

    def show_popup(self, title, text):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(text)

        # Set font for the popup text
        popup_font = QFont()
        popup_font.setPointSize(12)  # Set the font size for popup text
        popup_font.setBold(True)  # Make the popup text font bold
        msg_box.setFont(popup_font)

        # Center the text both vertically and horizontally
        msg_box.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        # Set the minimum width to accommodate the text
        msg_box.setMinimumWidth(400)

        msg_box.exec()
