from main_menu import StartScreen
from region_selection import RegionSelector
from date_selection import DateSelector
from factor_selection import FactorSelector
from flow_and_value import PlotFlow
from forecasting import ForecastFlow
from mod_forecast import SetupForecast

import database_example as ex_database

class TourismApp:

    def __init__(self, use_real_data, use_llm_analyzer):
        self.start_screen = None
        self.region_selector = None
        self.date_selector = None
        self.factor_selector = None
        self.flow_value = None
        self.setup = None
        self.forecast = None
        self.windows = []

        self.skip_eval = False
        self.areas = None
        self.period = None
        self.factors = None
        self.query = None

        self.gen_fac = None
        self.db = None
        self.tourist_flow = None
        self.area_flows = None
        self.steps = None

        """
            If you want to use real database, you need to fill the data for areas and dates
            you're going to use, otherwise the app will crush. That includes all values for factors.
            See fill_data_example.sql in db for example. If set False, random data will be generated.
        """
        self.use_database = use_real_data

        """
                    If you want to use llm analyzer, you must install ollama and the model you want to use,
                    by default it is gemma3, but you can change it in config file.
                """
        self.use_llm = use_llm_analyzer

        self.start_init = StartScreen(self)
        self.region_select_init = RegionSelector(self)
        self.date_select_init = DateSelector(self)
        self.factor_select_init = FactorSelector(self)
        self.flow_init = PlotFlow(self)
        self.setup_cast = SetupForecast(self)
        self.forecast_init = ForecastFlow(self)

    def run(self):
        self.run_start_menu()

    def run_start_menu(self):
        self.start_init.show_window()

    def run_region_selection(self):
        self.region_select_init.show_window()

    def run_date_selection(self):
        self.date_select_init.show_window()

    def run_factor_selector(self):
        self.factor_select_init.show_window()

    def run_plot_flow(self):
        self.flow_init.plot_flow_and_value()

    def run_setup_forecast(self):
        self.setup_cast.show_window()

    def run_forecast(self):
        self.forecast_init.forecast()

    def close(self):
        for window in self.windows:
            window.close()

    def init_database(self):
        self.db = ex_database.setup_data(self.use_database)

    def form_query(self):
        date_factors = {period: self.factors for period in self.period}
        self.query = {area: date_factors for area in self.areas}

    def set_window_titles(self):
        # Set consistent window titles
        app_name = "Анализ Туризма"  # Your app name here
        self.start_init.setWindowTitle(app_name)
        self.region_select_init.setWindowTitle(f"{app_name} - Выберите регионы")
        self.date_select_init.setWindowTitle(f"{app_name} - Выберите дату")
        self.factor_select_init.setWindowTitle(f"{app_name} - Выбор факторов на оценку")
        self.flow_init.setWindowTitle(f"{app_name} - Оценка потребительской ценности")
        self.setup_cast.setWindowTitle(f"{app_name} - Параметры прогнозирования")
        self.forecast_init.setWindowTitle(f"{app_name} - Результаты прогноза")