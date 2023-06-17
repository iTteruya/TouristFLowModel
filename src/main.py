import PySimpleGUI as sg
from first_window import FirstWindow
from second_window import SecondWindow
from factor_selection import FactorSelector
from flow_and_value import PlotFlow
from forecasting import ForecastFlow
from mod_forecast import SetupForecast

sg.theme("LightGray1")


class TourismApp:

    def __init__(self, use_real_database):
        self.first_window = None
        self.second_window = None
        self.factor_selector = None
        self.flow_value = None
        self.setup = None
        self.forecast = None
        self.windows = []

        self.areas = None
        self.period = None
        self.factors = None
        self.query = None

        self.gen_fac = None
        self.db = None
        self.tourist_flow = None
        self.steps = None

        """
        If you want to use real database, you need to fill the data for areas and dates
        you're going to use, otherwise the app will crush. That includes all values for factors.
        See fill_data_example.sql in db for example. If set False, random data will be generated.
        """
        self.use_database = use_real_database

        self.first_init = FirstWindow()
        self.second_init = SecondWindow()
        self.factor_select_init = FactorSelector()
        self.flow_init = PlotFlow(self.use_database)
        self.setup_cast = SetupForecast()
        self.forecast_init = ForecastFlow()

    def run(self):
        self.run_first_screen()

    def run_first_screen(self):
        self.first_init.show_first(self)

    def run_second_screen(self):
        self.second_init.show_second(self)

    def run_factor_selector(self):
        self.factor_select_init.select_factors(self)

    def run_plot_flow(self):
        self.flow_init.plot_flow_and_value(self)

    def run_setup_forecast(self):
        self.setup_cast.show_setup(self)

    def run_forecast(self):
        self.forecast_init.forecast(self)

    def close(self):
        for window in self.windows:
            window.close()

    def form_query(self):
        date_factors = {period: app.factors for period in app.period}
        self.query = {area: date_factors for area in app.areas}


if __name__ == "__main__":
    app = TourismApp(use_real_database=False)
    app.run()
