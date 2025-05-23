import copy
import numpy as np
import pyqtgraph as pg
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, QMainWindow, QHBoxLayout,
                             QPlainTextEdit, QMessageBox, QFileDialog)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from pyqtgraph import mkPen
from pyqtgraph.exporters import ImageExporter
from datetime import datetime
from config import colors

class PlotFlow(QMainWindow):

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.use_db = app.use_database
        self.plot_created = False
        self.cur_query = None
        self.flow = None
        self.area_flows = {}
        self.calculated_values = None
        self.alpha = 1.00
        self.beta = 1.00
        self.gamma = 1.00
        self.phi = 1.00
        self.omega = 1.00

        self.db = app.db

        self.init_ui()

    def init_ui(self):
        widget = QWidget()
        self.setCentralWidget(widget)

        layout = QVBoxLayout()

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        layout.addWidget(self.plot_widget)

        label = QLabel('Оценка влияния факторов: ')
        label.setFont(QFont('Helvetica', 16))
        layout.addWidget(label)

        self.values_text = QPlainTextEdit()
        self.values_text.setFont(QFont('Helvetica', 16))
        self.values_text.setReadOnly(True)
        layout.addWidget(self.values_text)

        self.mean_label = QLabel('')
        self.mean_label.setFont(QFont('Helvetica', 16))
        layout.addWidget(self.mean_label)

        button_layout0 = QHBoxLayout()

        calculate_button = QPushButton('Рассчитать')
        calculate_button.clicked.connect(self.calculate)
        button_layout0.addWidget(calculate_button)

        save_button = QPushButton('Сохранить результаты')
        save_button.clicked.connect(self.save_results)
        button_layout0.addWidget(save_button)

        layout.addLayout(button_layout0)

        button_layout1 = QHBoxLayout()
        self.button_home = QPushButton("Меню", self)
        self.button_home.clicked.connect(self.return_to_main)
        button_layout1.addWidget(self.button_home)

        back_button = QPushButton('Назад')
        back_button.clicked.connect(self.go_back)
        button_layout1.addWidget(back_button)

        next_button = QPushButton('Прогнозирование')
        next_button.clicked.connect(self.go_to_next)
        button_layout1.addWidget(next_button)

        layout.addLayout(button_layout1)

        widget.setLayout(layout)
        self.setMinimumSize(600, 600)
        self.resize(1280, 720)
        self.center_window()

    def center_window(self):
        screen_geometry = self.screen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    # Inside plot_flow_and_value method
    def plot_flow_and_value(self):
        self.show()

        if self.cur_query != self.app.query:
            if not self.use_db and len(self.app.period[0]) == 10:
                for area, area_data in self.app.query.items():
                    self.db.area[area].partial_fulldate(self.app.period)
            self.cur_query = copy.deepcopy(self.app.query)
            self.calculated_values = None

            self.area_flows = {}
            for area, area_data in self.cur_query.items():
                area_flow = []
                for date, date_data in area_data.items():
                    date_flow = self.db.area[area].date[date].tourist_flow
                    area_flow.append(date_flow)
                self.area_flows[area] = area_flow

            self.flow = [sum(items) for items in zip(*self.area_flows.values())]

            # Clear old plots
            self.plot_widget.clear()
            self.plot_widget.addLegend()

            self.plot_created = False
            self.plot_widget.clear()

        if self.plot_created:
            self.plot_widget.clear()

        if self.calculated_values is not None:
            calculated_values_text = '\n'.join(f"{value:.2f}" for value in self.calculated_values)
            self.values_text.setPlainText(calculated_values_text)

            mean_value = np.mean(self.calculated_values)
            self.mean_label.setText(f"Общая оценка: {mean_value:.2f}")

        self.plot_widget.setTitle('Оценка туристического потока')
        self.plot_widget.setLabel('bottom', text='Дата')
        self.plot_widget.setLabel('left', text='Туристический поток')

        self.plot_widget.showGrid(x=True, y=True)

        # Convert date strings to datetime objects with correct format
        # Set x-axis tick positions and labels
        if len(self.app.period[0]) == 10:
            x_axis_dates = [datetime.strptime(date, '%d-%m-%Y') for date in self.app.period]
            self.plot_widget.getAxis('bottom').setTicks(
                [[(i, date.strftime('%d-%m-%Y')) for i, date in enumerate(x_axis_dates)]])
        elif len(self.app.period[0]) == 7:
            x_axis_dates = [datetime.strptime(date, '%m-%Y') for date in self.app.period]
            self.plot_widget.getAxis('bottom').setTicks(
                [[(i, date.strftime('%m-%Y')) for i, date in enumerate(x_axis_dates)]])
        else:
            x_axis_dates = [datetime.strptime(date, '%Y') for date in self.app.period]
            self.plot_widget.getAxis('bottom').setTicks(
                [[(i, date.strftime('%Y')) for i, date in enumerate(x_axis_dates)]])

        x_values = list(range(len(self.app.period)))

        for i, (area, flow) in enumerate(self.area_flows.items()):
            color = colors[i % len(colors)]
            self.plot_widget.plot(x=x_values, y=flow, pen=mkPen(color=color, width=2), name=area)

        # Plot the overall total flow line in red
        if len(self.area_flows) > 1:
            self.plot_widget.plot(x=x_values, y=self.flow, pen=mkPen(color='r', width=3), name='Общий поток')
        self.plot_created = True

    def save_results(self):
        if not self.calculated_values:
            self.show_warning_message("Нет данных для сохранения.")
            return

        # Ask user where to save
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить результаты", "", "Text Files (*.txt)")
        if file_path:
            # Save textual results
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.values_text.toPlainText())
                    file.write('\n' + ('_' * 80) + '\n')
                    file.write(self.mean_label.text())
            except Exception as e:
                self.show_warning_message(f"Ошибка при сохранении файла: {str(e)}")
                return

            # Try saving plot image
            try:
                exporter = ImageExporter(self.plot_widget.plotItem)
                image_path = file_path.rsplit('.', 1)[0] + '.png'
                exporter.export(image_path)
            except Exception as e:
                self.show_warning_message(f"Текст сохранён, но ошибка при сохранении графика: {str(e)}")
                return

            QMessageBox.information(self, "Сохранение завершено", "Результаты и график успешно сохранены.")

    def return_to_main(self):
        self.hide()
        self.app.run_start_menu()

    def go_back(self):
        self.hide()
        self.app.run_factor_selector()

    def go_to_next(self):
        self.app.tourist_flow = self.flow
        self.app.area_flows = self.area_flows
        self.app.db = self.db
        self.hide()
        self.app.run_setup_forecast()

    def calculate(self):
        if self.cur_query is None or len(self.cur_query) == 0:
            self.show_warning_message("Нет данных для расчета")
            return

        factor_sums = {}  # area -> date -> factor -> segment value
        factor_details = {}  # area -> date -> factor -> subfactor -> value

        # Collect subfactor values and segment products
        for area, area_data in self.cur_query.items():
            if area not in factor_sums:
                factor_sums[area] = {}
                factor_details[area] = {}

            for date, date_data in area_data.items():
                if date not in factor_sums[area]:
                    factor_sums[area][date] = {}
                    factor_details[area][date] = {}

                for factor, subfactors in date_data.items():
                    product = 1.0
                    factor_details[area][date][factor] = {}

                    for subfactor in subfactors:
                        value = float(self.db.area[area].date[date].factors[factor][subfactor])
                        product += value
                        factor_details[area][date][factor][subfactor] = value

                    factor_sums[area][date][factor] = product

        # Calculate scores per area
        area_scores = {}
        text_lines = []

        for area, date_data in factor_sums.items():
            area_scores[area] = []
            text_lines.append('_' * 80)
            text_lines.append(area)
            text_lines.append('_' * 80)

            for date, factor_data in date_data.items():
                if len(factor_data) != 5:
                    self.show_warning_message(f"Недостаточно факторов для {area} на дату {date}")
                    return
                try:
                    ti = factor_data['Транспортный сегмент'] ** self.alpha
                    ac = factor_data['Сегмент размещения'] ** self.beta
                    lr = factor_data['Сегмент отдыха и развлечений'] ** self.gamma
                    fs = factor_data['Пищевой сегмент'] ** self.phi
                    of = factor_data['Другие факторы'] ** self.omega

                    score = (ti * ac * lr * fs * of) ** (1 / 5)
                    final_score = round(score, 2)
                except KeyError as e:
                    self.show_warning_message(f"Отсутствует фактор {e} для {area} на дату {date}")
                    return

                area_scores[area].append(final_score)

                # Start result line
                text_lines.append(f"{date} - {area} - Общая оценка: {final_score:.2f};")

                # Add segment values
                for factor_code, segment_value in factor_data.items():
                    text_lines.append(f"  {factor_code} - Оценка сегмента: {round(segment_value, 2)};")
                    for subfactor_name, val in factor_details[area][date][factor_code].items():
                        text_lines.append(f"    {factor_code} - {subfactor_name} - Оценка фактора: {val:.2f};")

        self.calculated_values = area_scores

        # Add combined score if multiple areas
        if len(area_scores) > 1:
            text_lines.append('_' * 80)
            text_lines.append('Общий поток')
            text_lines.append('_' * 80)
            combined_scores = []
            for i in range(len(self.app.period)):
                values_at_i = [scores[i] for scores in area_scores.values()]
                combined_score = round(np.mean(values_at_i), 2)
                combined_scores.append(combined_score)
                text_lines.append(f"{self.app.period[i]} - Общий поток - Общая оценка: {combined_score:.2f};")
            self.calculated_values['Общий'] = combined_scores

            mean_value = np.mean(combined_scores)
        else:
            only_area = next(iter(area_scores))
            mean_value = np.mean(area_scores[only_area])

        self.values_text.setPlainText('\n'.join(text_lines))
        self.mean_label.setText(f"Общая оценка: {mean_value:.2f}")

    def show_warning_message(self, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Предупреждение")

        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        msg_box.setFont(font)

        msg_label = QLabel(message)
        msg_label.setFont(font)
        msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg_box.layout().addWidget(msg_label, 0, 0, 1, msg_box.layout().columnCount(), Qt.AlignmentFlag.AlignCenter)

        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()  # Note the use of exec_() instead of exec()

    def closeEvent(self, event):
        self.app.close()