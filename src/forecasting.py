import copy
import numpy as np
import pandas as pd
import pyqtgraph as pg
from PyQt6.QtCore import Qt, QRunnable, QThreadPool, QObject, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMainWindow, QHBoxLayout, QTextEdit, QApplication, \
    QMessageBox, QFileDialog, QLabel
from pyqtgraph import mkPen, InfiniteLine
from pyqtgraph.exporters import ImageExporter
from statsmodels.tsa.statespace.sarimax import SARIMAX
from config import colors, setup_forecast_analyzer_rus, setup_forecast_analyzer_eng, report_example
import random

class LLMWorkerSignals(QObject):
    finished = pyqtSignal(str)           # final report text
    error   = pyqtSignal(str)            # error string (optional)

class LLMWorker(QRunnable):
    """
    Runs the LLM report generation in a separate thread.
    """
    def __init__(self, summary: str, lang: str = "eng"):
        super().__init__()
        self.summary = summary
        self.lang = lang
        self.signals = LLMWorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            if self.lang == "rus":
                result = setup_forecast_analyzer_rus(self.summary)
            else:
                result = setup_forecast_analyzer_eng(self.summary)
            self.signals.finished.emit(str(result))
        except Exception as e:
            self.signals.error.emit(str(e))

def generate_future_exog(app):
    exog_future_num = []
    exog_future_val = []

    for factor, data in app.gen_fac.items():
        num_val = []
        fac_val = []
        delta = data['delta_value']

        if data['section'] == "Количественные факторы":
            for i in range(app.steps):
                if data['selected_option'] == 'Up':
                    value = data['value'] + delta * i
                elif data['selected_option'] == 'Down':
                    value = data['value'] - delta * i
                else:
                    delta_var = random.choice([delta, -delta])
                    value = data['value'] + delta_var * i

                num_val.append(value)
        else:
            for i in range(app.steps):
                if data['selected_option'] == 'Up':
                    value = data['value'] + delta * i
                elif data['selected_option'] == 'Down':
                    value = data['value'] - delta * i
                else:
                    delta_var = random.choice([delta, -delta])
                    value = data['value'] + delta_var * i

                fac_val.append(value)

        if fac_val:
            exog_future_val.append(fac_val)
        if num_val:
            exog_future_num.append(num_val)

    all_gen = None
    if exog_future_val and exog_future_num:
        all_gen = np.concatenate((exog_future_val, exog_future_num), axis=0)
    elif exog_future_val:
        all_gen = exog_future_val
    else:
        all_gen = exog_future_num

    return all_gen


def prepare_train_data(app):
    date = str(app.period[0])

    if len(date) == 4:
        all_dates = app.db.area['Российская Федерация'].years_list
    elif len(date) == 7:
        all_dates = app.db.area['Российская Федерация'].months_list
    else:
        all_dates = app.db.area['Российская Федерация'].fulldate_list

    flow_data = []
    factor_data = []
    num_factor_date = []

    for area, area_data in app.query.items():
        area_flow = []
        area_fac = []
        area_num_fac = []

        for date in all_dates:
            date_flow = app.db.area[area].date[date].tourist_flow
            area_flow.append(date_flow)
            date_fac = []
            date_num = []
            for factor, data in app.gen_fac.items():
                if data['section'] == "Количественные факторы":
                    factor_val = app.db.area[area].date[date].num_factors[factor]
                    date_num.append(factor_val)
                else:
                    factor_val = app.db.area[area].date[date].factors[data['section']][factor]
                    date_fac.append(factor_val)
            area_fac.append(date_fac)
            area_num_fac.append(date_num)
        flow_data.append(area_flow)
        factor_data.append(list(zip(*area_fac)))
        num_factor_date.append(list(zip(*area_num_fac)))

    all_factors = None
    list_3d_float = np.array(num_factor_date, dtype=float)
    num_factor_mean = np.sum(list_3d_float, axis=0)

    list_3d_float = np.array(factor_data, dtype=float)  # Convert strings to floats
    factors_mean = np.mean(list_3d_float, axis=0)

    if num_factor_mean.any() and factors_mean.any():
        all_factors = np.concatenate((factors_mean, num_factor_mean), axis=0)
    elif num_factor_mean.any():
        all_factors = num_factor_mean
    else:
        all_factors = factors_mean

    flow = [sum(items) for items in zip(*flow_data)]
    return flow, all_factors


def generate_var(original_df, num_rows, delta):
    num_cols = len(original_df.columns)
    new_data = []

    for _ in range(num_rows):
        row = []
        for col_idx in range(num_cols):
            original_values = original_df.iloc[:, col_idx]
            original_mean = original_values.mean()
            deviation = original_mean * delta / 100.0
            new_value = original_mean + random.uniform(-deviation, deviation)
            row.append(new_value)

        new_data.append(row)

    new_df = pd.DataFrame(new_data, columns=original_df.columns)
    return new_df


def get_all_factors(database, query):
    factor_sums = {}
    for area, area_data in query.items():
        if area not in factor_sums:
            factor_sums[area] = {}

        for date, date_data in area_data.items():
            if date not in factor_sums[area]:
                factor_sums[area][date] = {}

            for factor, factor_data in date_data.items():
                if factor not in factor_sums[area][date]:
                    factor_sums[area][date][factor] = 1.0

                for subfactor in factor_data:
                    value = database.area[area].date[date].factors[factor][subfactor]
                    factor_sums[area][date][factor] += float(value)

    values = []
    for area, area_data in factor_sums.items():
        area_value = []
        for date, date_data in area_data.items():
            date_value = []
            for factor, sum_value in date_data.items():
                date_value.append(sum_value)
            area_value.append(date_value)
        values.append(area_value)

    factors_mean = [list(map(lambda x: sum(x) / len(x), zip(*sublists))) for sublists in zip(*values)]
    transposed_factors = list(zip(*factors_mean))

    def calculate_total_factors(db, qu):
        date_factors = {}

        for area, date_model in db.area.items():
            if area in qu:
                for date, factors_set in date_model.date.items():
                    if date in qu[area]:
                        if date not in date_factors:
                            date_factors[date] = factors_set.num_factors.copy()
                        else:
                            for factor, value in factors_set.num_factors.items():
                                date_factors[date][factor] += value

        return date_factors

    # Calculate the sum of num_factors for the specified areas and dates
    total_factors = calculate_total_factors(database, query)

    # Print the result
    num_value = []
    for date, factors in total_factors.items():
        date_val = []
        for factor, value in factors.items():
            date_val.append(value)
        num_value.append(date_val)

    transposed_num = list(zip(*num_value))

    return [*transposed_factors, *transposed_num]


from datetime import datetime, timedelta

def generate_future_dates(date_string, num_steps):
    formats = ["%d-%m-%Y", "%m-%Y", "%Y"]  # Supported date formats

    for date_format in formats:
        try:
            date = datetime.strptime(date_string, date_format)
            break
        except ValueError:
            continue
    else:
        # Check if the input is a year format ("%Y")
        if len(date_string) == 4:
            date_format = "%Y"
            date = datetime.strptime(date_string, date_format)
        else:
            raise ValueError("Invalid date format")

    future_dates = []
    for _ in range(num_steps):
        future_dates.append(date.strftime(date_format))
        if date_format == "%Y":
            date = date.replace(year=date.year + 1)  # Increment the year by one
        elif date_format == "%m-%Y":
            if date.month == 12:
                date = date.replace(year=date.year + 1, month=1)
            else:
                date = date.replace(month=date.month + 1)
        else:
            date = date + timedelta(days=1)

    return future_dates


def forecast_flow(app, cur_flow, use_all):
    if use_all:
        train_data = pd.DataFrame({'tourist_flow': cur_flow})
        all_factors = get_all_factors(app.db, app.query)
    else:
        flow, all_factors = prepare_train_data(app)
        train_data = pd.DataFrame({'tourist_flow': flow})

    endog = train_data['tourist_flow']
    exog_df = pd.DataFrame(list(zip(*all_factors)))

    # 🧠 [DUMMY PLACEHOLDER] Insert AI-enhanced exogenous feature transformation or selection
    exog_df = apply_future_ai_model(exog_df, app)

    model = SARIMAX(endog, exog=exog_df, order=(1, 0, 0), seasonal_order=(0, 0, 0, 0))
    model_fit = model.fit(method='bfgs', maxiter=1000)

    if use_all:
        delta = 5
        future_exog_df = generate_var(exog_df, app.steps, delta)
    else:
        future_ex = generate_future_exog(app)
        future_exog_df = pd.DataFrame(list(zip(*future_ex)))

    # 🧠 [DUMMY PLACEHOLDER] Apply AI to refine future exogenous features
    future_exog_df = refine_future_exog_with_ai(future_exog_df, app)

    forecast = model_fit.get_forecast(steps=app.steps, exog=future_exog_df)
    forecast_values = forecast.predicted_mean
    confidence_intervals = forecast.conf_int()

    return forecast_values, confidence_intervals

class ForecastFlow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.analyzer_report = None
        self.plot_created = False  # Flag to track if the plot has been created
        self.real_flow = {}
        self.forecast_flow = {}
        self.confidence_intervals = {}
        self.steps = None
        self.db = None
        self.period = None
        self.area_flows = {}
        self.overall_flow = None
        self.thread_pool = QThreadPool.globalInstance()

        # Use all factors to train model, might generate gibberish
        self.use_all = True
        self.gen_fac = None

        # Store the main application reference
        self.app = app

        # Create the main widget and layout
        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)

        # Create a plot widget from PyQtGraph
        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)

        # Report display area (multiline text box, read-only)
        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)
        self.report_text.setPlaceholderText("Для формирования отчета и рекомендаций начните анализ результатов")
        self.layout.addWidget(self.report_text)  # Add between plot and buttons

        button_layout0 = QHBoxLayout()

        self.analyze_button = QPushButton("Анализ результатов и формирование рекомендаций", self)
        self.analyze_button.clicked.connect(self.llm_analyze)
        button_layout0.addWidget(self.analyze_button)

        self.save_button = QPushButton('Сохранить результаты')
        self.save_button.clicked.connect(self.save_results)
        button_layout0.addWidget(self.save_button)

        self.layout.addLayout(button_layout0)

        # Add exit and back buttons
        self.home_button = QPushButton('Меню')
        self.back_button = QPushButton('Назад')

        button_layout1 = QHBoxLayout()
        button_layout1.addWidget(self.home_button)
        button_layout1.addWidget(self.back_button)
        self.layout.addLayout(button_layout1)

        # Connect button signals
        self.home_button.clicked.connect(self.return_to_main)
        self.back_button.clicked.connect(self.go_back)

        # Initialize the plot
        self.plot = self.plot_widget.plot()
        self.plot_widget.setTitle("Предсказанный поток")
        self.plot_widget.setLabel('bottom', 'Дата')
        self.plot_widget.setLabel('left', 'Туристический поток')
        self.plot_widget.showGrid(x=True, y=True)
        self.plot_widget.setBackground('w')  # Set plot background to white

    def llm_analyze(self):

        # Example: gather forecast result summary

        forecast_data_summary_example = """
                Area: Downtown
                Dates: 2024-01 to 2024-12
                Top Factors: [Weather Index: 0.32, Holiday Events: 0.28, Hotel Prices: -0.15, Marketing Score: 0.10, Public Transport Availability: 0.08]
                Forecasted Tourist Flow (2024-06): 120,000 (CI: 110,000 – 130,000)
                Observed Flow (2024-06): 125,000
                ...

                Area: Beachfront
                ...
                """

        #Replace with actual analyzer
        analyze_forecasting_results(self.forecast_flow, self.app)

        forecast_data_summary = ""
        for area, forecast in self.forecast_flow.items():
            mean_val = forecast.mean()
            forecast_data_summary += f"Область: {area}, Среднее прогнозируемое значение: {mean_val:.2f}\n"

        if self.app.use_llm:
            # UI feedback
            self.report_text.setPlainText("🔄 Генерация отчёта… Пожалуйста, подождите.")
            self.analyze_button.setEnabled(False)
            QApplication.processEvents()

            # create worker and wire signals
            worker = LLMWorker(forecast_data_summary, lang="rus")  # or "eng"
            worker.signals.finished.connect(self._llm_done)
            worker.signals.error.connect(self._llm_error)

            self.thread_pool.start(worker)
        else:
            self.report_text.setPlainText(report_example)
            self.analyzer_report = report_example

    def _llm_done(self, report: str):
        self.report_text.setPlainText(report)
        self.analyzer_report = report
        self.analyze_button.setEnabled(True)

    def _llm_error(self, msg: str):
        self.report_text.setPlainText(f"❌ Ошибка LLM: {msg}")
        self.analyzer_report = msg
        self.analyze_button.setEnabled(True)

    def return_to_main(self):
        self.app.forecast.hide()
        self.app.run_start_menu()

    def go_back(self):
        self.app.forecast.hide()
        self.app.run_setup_forecast()

    def show_window(self):
        self.app.forecast.show()
        self.plot_forecast()

    def save_results(self):
        if not self.analyzer_report:
            self.show_warning_message("Нет данных для сохранения.")
            return

        # Ask user where to save
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить результаты", "", "Text Files (*.txt)")
        if file_path:
            # Save textual results
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.analyzer_report)
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

    def plot_forecast(self):
        self.area_flows.clear()
        self.forecast_flow.clear()
        self.confidence_intervals.clear()

        if self.steps != self.app.steps or self.gen_fac != self.app.gen_fac:
            self.gen_fac = copy.deepcopy(self.app.gen_fac)
            # Get tourist flow
            self.real_flow = self.app.area_flows

            self.plot_created = False
            self.plot.clear()

            self.period = [*self.app.period, *generate_future_dates(self.app.period[-1], self.app.steps)]

            for (area, flow) in self.real_flow.items():
                self.forecast_flow[area], self.confidence_intervals[area] = forecast_flow(self.app, flow, self.use_all)
                self.area_flows[area] = [*self.real_flow[area], *self.forecast_flow[area]]

        self.overall_flow = [sum(items) for items in zip(*self.area_flows.values())]

        # Clear old plots
        self.plot_widget.clear()
        self.plot_widget.addLegend()

        self.plot_created = False
        self.plot_widget.clear()

        self.plot_widget.setTitle('Прогноз туристического потока')
        self.plot_widget.setLabel('bottom', text='Дата')
        self.plot_widget.setLabel('left', text='Туристический поток')

        if len(self.app.period[0]) == 10:
            x_axis_dates = [datetime.strptime(date, '%d-%m-%Y') for date in self.period]
            self.plot_widget.getAxis('bottom').setTicks(
                [[(i, date.strftime('%d-%m-%Y')) for i, date in enumerate(x_axis_dates)]])
        elif len(self.app.period[0]) == 7:
            x_axis_dates = [datetime.strptime(date, '%m-%Y') for date in self.period]
            self.plot_widget.getAxis('bottom').setTicks(
                [[(i, date.strftime('%m-%Y')) for i, date in enumerate(x_axis_dates)]])
        else:
            x_axis_dates = [datetime.strptime(date, '%Y') for date in self.period]
            self.plot_widget.getAxis('bottom').setTicks(
                [[(i, date.strftime('%Y')) for i, date in enumerate(x_axis_dates)]])

        x_values = list(range(len(self.period)))

        split_index = len(self.app.period) - 1
        vline = InfiniteLine(pos=split_index, angle=90, movable=False, pen=mkPen(color='magenta', width=3, style=Qt.PenStyle.DashLine))
        self.plot_widget.addItem(vline)

        for i, (area, flow) in enumerate(self.area_flows.items()):
            color = colors[i % len(colors)]
            self.plot_widget.plot(x=x_values, y=flow, pen=mkPen(color=color, width=2), name=area)

        if len(self.area_flows) > 1:
            self.plot_widget.plot(x=x_values, y=self.overall_flow, pen=mkPen(color='r', width=3), name='Общий поток')

        self.plot_created = True

    def create_window(self):
        self.app.forecast = QMainWindow()
        self.app.forecast.setWindowTitle(self.windowTitle())
        self.app.forecast.setMinimumSize(600, 600)
        self.app.forecast.resize(1280, 720)

        self.app.forecast.setCentralWidget(self.central_widget)

        # Center the window
        screen_geometry = self.app.forecast.screen().geometry()
        x = int((screen_geometry.width() - self.app.forecast.width()) / 2)
        y = int((screen_geometry.height() - self.app.forecast.height()) / 2)
        self.app.forecast.move(x, y)

        self.app.windows.append(self.app.forecast)

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

    def forecast(self):
        self.create_window()
        self.show_window()

    def closeEvent(self, event):
        self.app.close()


def analyze_forecasting_results(forecasting_results, app):
    """
    Dummy placeholder for analyzing forecasting results.
    """
    # TODO: Replace this with actual analyzer logic
    return forecasting_results

def apply_future_ai_model(exog_df, app):
    """
    Dummy placeholder for AI-based preprocessing, feature selection or embedding generation.
    """
    # TODO: Replace this with actual AI-enhanced logic (e.g., PCA, autoencoder, neural embedding, etc.)
    return exog_df


def refine_future_exog_with_ai(future_exog_df, app):
    """
    Dummy placeholder for AI-based future exogenous feature refinement.
    """
    # TODO: Implement AI methods like generative models, boosting, etc., for future feature improvement
    return future_exog_df