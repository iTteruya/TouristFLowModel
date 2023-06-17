import copy
import PySimpleGUI as sg
import pandas as pd
from datetime import datetime, timedelta
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import random
import numpy as np


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
            date = date + timedelta(days=1)
        elif date_format == "%m-%Y":
            if date.month == 12:
                date = date.replace(year=date.year + 1, month=1)
            else:
                date = date.replace(month=date.month + 1)
        else:
            date = date + timedelta(days=1)

    return future_dates


def forecast_flow(app, use_all):
    if use_all:
        # Create a DataFrame with the flow values
        train_data = pd.DataFrame({'tourist_flow': app.tourist_flow})
        all_factors = get_all_factors(app.db, app.query)
    else:
        flow, all_factors = prepare_train_data(app)
        train_data = pd.DataFrame({'tourist_flow': flow})

    # Assign the flow values to the endogenous variable
    endog = train_data['tourist_flow']
    exog_df = pd.DataFrame(list(zip(*all_factors)))

    model = SARIMAX(endog, exog=exog_df, order=(1, 0, 0), seasonal_order=(0, 0, 0, 0),
                    start_params=[0.5, 0.5, 0.5, 0.5], method='bfgs', maxiter=1000)
    model_fit = model.fit()

    if use_all:
        delta = 5
        future_exog_df = generate_var(exog_df, app.steps, delta)
    else:
        future_ex = generate_future_exog(app)
        future_exog_df = pd.DataFrame(list(zip(*future_ex)))

    forecast = model_fit.get_forecast(steps=app.steps, exog=future_exog_df)

    # Get the forecasted values
    forecast_values = forecast.predicted_mean

    # Get the confidence intervals for the forecast
    confidence_intervals = forecast.conf_int()

    return forecast_values, confidence_intervals


class ForecastFlow:
    def __init__(self):
        self.plot_created = False  # Flag to track if the plot has been created
        self.real_flow = None
        self.forecast_flow = None
        self.confidence_intervals = None
        self.steps = None
        self.db = None
        self.period = None
        self.all_flow = None

        # Use all factors to train model, might generate gibberish
        self.use_all = True
        self.gen_fac = None

        # Create the plot
        self.fig, self.ax = plt.subplots()

    def create_window(self):
        layout = [
            [sg.Canvas(key='-CANVAS-', expand_x=True, expand_y=True)],
            [sg.Button('Выход'), sg.Button("Назад")]
        ]

        window = sg.Window('Туристический поток', layout, finalize=True, resizable=True)

        # Set a suitable window size
        window_size = (900, 900)  # Adjust the width as needed
        window.TKroot.geometry(f"{window_size[0]}x{window_size[1]}")

        # Center the window
        window.TKroot.update_idletasks()  # Ensure the window has the correct size before centering
        width, height = window.TKroot.winfo_width(), window.TKroot.winfo_height()
        screen_width, screen_height = window.TKroot.winfo_screenwidth(), window.TKroot.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.TKroot.geometry(f"{width}x{height}+{x}+{y}")

        return window

    def forecast(self, app):
        # Create the window
        app.forecast = self.create_window()
        app.windows.append(app.forecast)

        if self.steps != app.steps or self.gen_fac != app.gen_fac:
            self.gen_fac = copy.deepcopy(app.gen_fac)
            # Get tourist flow
            self.real_flow = app.tourist_flow

            self.plot_created = False
            self.ax.clear()

        # Clear previous plot if it was created
        if self.plot_created:
            self.ax.clear()  # Clear the axes

        self.forecast_flow, self.confidence_intervals = forecast_flow(app, self.use_all)
        self.period = [*app.period, *generate_future_dates(app.period[-1], app.steps)]

        self.all_flow = [*self.real_flow, *self.forecast_flow]
        # Draw the new plot
        self.ax.set_title('Предсказанный поток')
        self.ax.set_xlabel('Дата')
        self.ax.set_ylabel('Туристический поток')
        self.ax.plot(self.period, self.all_flow)

        if len(app.period[0]) == 10 or len(self.period) > 20:
            # Set x-axis tick positions to display every 12th x-value
            skip = int(len(self.period) / 6)
            self.ax.set_xticks(self.period[::skip])

        # Fill the confidence intervals
        # self.ax.fill_between(generate_future_dates(app.period[-1], app.steps), self.confidence_intervals.iloc[:, 0],
        #                 self.confidence_intervals.iloc[:, 1], alpha=0.2)

        # Draw the plot on the canvas
        canvas = FigureCanvasTkAgg(self.fig, master=app.forecast['-CANVAS-'].TKCanvas)
        canvas.draw()

        # Add the canvas to the layout
        canvas.get_tk_widget().pack(fill='both', expand=True)

        toolbar = NavigationToolbar2Tk(canvas, app.forecast['-CANVAS-'].TKCanvas)
        toolbar.update()

        self.plot_created = True

        # Event loop
        while True:
            event, values = app.forecast.read()

            if event == sg.WINDOW_CLOSED or event == 'Выход':
                break

            elif event == "Назад":
                app.forecast.hide()
                app.run_setup_forecast()

        # Close the window
        app.close()
