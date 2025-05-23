from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QLabel, QMessageBox, QApplication, \
    QHBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from config import trans_infr, acc_seg, food_seg, rr, other

class FactorSelector(QWidget):

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.selected_items = {
            "Транспортный сегмент": [],
            "Сегмент размещения": [],
            "Сегмент отдыха и развлечений": [],
            "Пищевой сегмент": [],
            "Другие факторы": []
        }

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()  # Top-level: vertical

        top_layout = QHBoxLayout()  # Horizontal row of lists
        category_list_layout = QVBoxLayout()  # All your categories go here

        # Add categories to the left side
        self.add_category(category_list_layout, "Транспортный сегмент", trans_infr)
        self.add_category(category_list_layout, "Сегмент размещения", acc_seg)
        self.add_category(category_list_layout, "Сегмент отдыха и развлечений", food_seg)
        self.add_category(category_list_layout, "Пищевой сегмент", rr)
        self.add_category(category_list_layout, "Другие факторы", other)

        # Right side: selected items
        selected_items_layout = QVBoxLayout()
        selected_label = QLabel("Выбранные факторы")
        selected_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.selected_display = QListWidget(self)
        self.selected_display.setFont(QFont("Arial", 12))

        selected_items_layout.addWidget(selected_label)
        selected_items_layout.addWidget(self.selected_display)

        # Add both columns to the top layout
        top_layout.addLayout(category_list_layout, 3)
        top_layout.addLayout(selected_items_layout, 2)

        main_layout.addLayout(top_layout)  # Add the top row to the main layout

        # --- BUTTONS BELOW ---
        button_font = QFont()
        button_font.setPointSize(14)
        button_font.setBold(True)

        button_row1 = QHBoxLayout()
        self.clear_button = QPushButton("Очистить", self)
        self.clear_button.setFont(button_font)
        self.clear_button.clicked.connect(self.clear_selection)
        button_row1.addWidget(self.clear_button)

        self.select_button = QPushButton("Выбрать", self)
        self.select_button.setFont(button_font)
        self.select_button.clicked.connect(self.select_items)
        button_row1.addWidget(self.select_button)

        button_row2 = QHBoxLayout()
        self.button_home = QPushButton("Меню", self)
        self.button_home.setFont(button_font)
        self.button_home.clicked.connect(self.return_to_main)
        button_row2.addWidget(self.button_home)

        self.back_button = QPushButton("Назад", self)
        self.back_button.setFont(button_font)
        self.back_button.clicked.connect(self.go_back)
        button_row2.addWidget(self.back_button)

        self.next_button = QPushButton("Далее", self)
        self.next_button.setFont(button_font)
        self.next_button.clicked.connect(self.go_to_next)
        button_row2.addWidget(self.next_button)

        # Add both button rows to the main layout
        main_layout.addLayout(button_row1)
        main_layout.addLayout(button_row2)

        self.setLayout(main_layout)
        self.setMinimumSize(450, 350)
        self.resize(1280, 720)

    def add_category(self, layout, category, items):
        font = QFont("Helvetica", 12, QFont.Weight.Bold)
        label = QLabel(category)
        label.setFont(font)
        layout.addWidget(label)

        list_widget = QListWidget(self)
        list_widget.addItems(items)
        list_widget.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        list_widget.setObjectName(category)

        # Set item font
        item_font = QFont()
        item_font.setPointSize(12)
        item_font.setBold(False)

        for index in range(list_widget.count()):
            list_widget.item(index).setFont(item_font)

        layout.addWidget(list_widget)

    def clear_selection(self):
        for category in self.selected_items.keys():
            list_widget = self.findChild(QListWidget, category)
            if list_widget:
                list_widget.clearSelection()
        self.selected_items = {key: [] for key in self.selected_items.keys()}
        self.selected_display.clear()

    def select_items(self):
        for category in self.selected_items.keys():
            list_widget = self.findChild(QListWidget, category)
            if list_widget:
                selected_items = [item.text() for item in list_widget.selectedItems()]
                self.selected_items[category] = selected_items
        self.show_selected_items()

    def show_selected_items(self):
        self.selected_display.clear()
        for category, items in self.selected_items.items():
            if items:
                self.selected_display.addItem(f"{category}:")
                for item in items:
                    self.selected_display.addItem(f"  • {item}")
                self.selected_display.addItem("")  # Spacer line

    def return_to_main(self):
        self.hide()
        self.app.run_start_menu()

    def go_back(self):
        self.hide()
        self.app.run_date_selection()

    def go_to_next(self):
        if any(self.selected_items.values()):
            self.hide()
            self.app.factors = self.selected_items
            self.app.form_query()
            self.app.run_plot_flow()
        else:
            self.show_warning_message("Пожалуйста, выберите хотя бы 1 фактор")

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
