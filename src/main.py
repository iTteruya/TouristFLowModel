import PySimpleGUI as sg
from first_window import FirstWindow
from second_window import SecondWindow
from factor_selection import FactorSelector
from flow_and_value import PlotFlow
from forecasting import ForecastFlow
from mod_forecast import SetupForecast

sg.theme("LightGray1")

first_init = FirstWindow()
second_init = SecondWindow()
second_init_opt3 = SecondWindow()
factor_select_init = FactorSelector()
forecast_init = ForecastFlow()
flow_init = PlotFlow()
setup_cast = SetupForecast()


class TourismApp:

    def __init__(self):
        # List of countries
        self.second_window = None
        self.first_window = None
        self.factor_selector = None
        self.flow_value = None
        self.setup = None
        self.forecast = None
        self.windows = []

        self.areas = None
        self.period = None
        self.factors = None
        self.query = None

        self.db = None
        self.tourist_flow = None
        self.steps = None

    def run(self):
        self.run_first_screen()

    def run_first_screen(self):
        first_init.show_first(self)

    def run_second_screen(self):
        second_init.show_second(self)

    def run_factor_selector(self):
        factor_select_init.select_factors(self)

    def run_plot_flow(self):
        flow_init.plot_flow_and_value(self)

    def run_setup_forecast(self):
        setup_cast.show_setup(self)

    def run_forecast(self):
        forecast_init.forecast(self)

    def close(self):
        for window in self.windows:
            window.close()

    def form_query(self):
        date_factors = {period: app.factors for period in app.period}
        self.query = {area: date_factors for area in app.areas}


if __name__ == "__main__":
    app = TourismApp()
    app.run()
