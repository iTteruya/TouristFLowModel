import copy
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import ex_database


class PlotFlow:
    def __init__(self):
        self.plot_created = False  # Flag to track if the plot has been created
        self.cur_query = None
        self.flow = None
        self.calculated_values = None
        self.alpha = 1.00
        self.beta = 1.00
        self.gamma = 1.00
        self.phi = 1.00
        self.omega = 1.00

        self.db = ex_database.DatabaseModel()

        # Create the plot
        self.fig, self.ax = plt.subplots()
        self.ax.set_title('Оценка туристического потока')
        self.ax.set_xlabel('Дата')
        self.ax.set_ylabel('Туристический поток')

    def create_window(self):
        layout = [
            [sg.Canvas(key='-CANVAS-', expand_x=True, expand_y=True)],
            [sg.Text('Оценка влияния факторов: ', font=('Helvetica', 16))],
            [sg.Multiline('', key='-VALUES-', size=(30, 6), font=('Helvetica', 16), disabled=True)],
            [sg.Text('', key='-MEAN-', size=(30, 1), font=('Helvetica', 16))],
            [sg.Button('Рассчитать', key='-CALCULATE-')],
            [sg.Button('Выход'), sg.Button("Назад"), sg.Button("Далее")]
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

    def plot_flow_and_value(self, app):
        # Create the window
        app.flow_value = self.create_window()
        app.windows.append(app.flow_value)

        if self.cur_query != app.query:
            self.cur_query = copy.deepcopy(app.query)
            self.calculated_values = None
            # Get tourist flow
            flow_data = []
            for area, area_data in self.cur_query.items():
                area_flow = []
                for date, date_data in area_data.items():
                    date_flow = self.db.area[area].date[date].tourist_flow
                    area_flow.append(date_flow)
                flow_data.append(area_flow)

            self.flow = [sum(items) for items in zip(*flow_data)]

            self.plot_created = False
            self.ax.clear()

        # Clear previous plot if it was created
        if self.plot_created:
            self.ax.clear()  # Clear the axes

        if self.calculated_values is not None:
            calculated_values_text = '\n'.join(f"{value:.2f}" for value in self.calculated_values)
            app.flow_value['-VALUES-'].update(calculated_values_text)

            mean_value = np.mean(self.calculated_values)
            app.flow_value['-MEAN-'].update(f"Общая оценка: {mean_value:.2f}")

        # Draw the new plot
        self.ax.plot(app.period, self.flow)

        # Draw the plot on the canvas
        canvas = FigureCanvasTkAgg(self.fig, master=app.flow_value['-CANVAS-'].TKCanvas)
        canvas.draw()
        canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

        toolbar = NavigationToolbar2Tk(canvas, app.flow_value['-CANVAS-'].TKCanvas)
        toolbar.update()
        canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

        self.plot_created = True

        # Event loop
        while True:
            event, values = app.flow_value.read()

            if event == sg.WINDOW_CLOSED or event == 'Выход':
                break

            elif event == "Назад":
                app.flow_value.hide()
                app.run_factor_selector()

            elif event == "Далее":
                app.tourist_flow = self.flow
                app.db = self.db
                app.flow_value.hide()
                app.run_setup_forecast()

            if event == '-CALCULATE-':
                if self.calculated_values is None:
                    # Perform calculations
                    factor_sums = {}
                    for area, area_data in self.cur_query.items():
                        if area not in factor_sums:
                            factor_sums[area] = {}

                        for date, date_data in area_data.items():
                            if date not in factor_sums[area]:
                                factor_sums[area][date] = {}

                            for factor, factor_data in date_data.items():
                                if factor not in factor_sums[area][date]:
                                    factor_sums[area][date][factor] = 1.0

                                for subfactor in factor_data:
                                    value = self.db.area[area].date[date].factors[factor][subfactor]
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

                    self.calculated_values = []
                    for factor_values in factors_mean:
                        ti_value = factor_values[0] ** self.alpha
                        as_value = factor_values[1] ** self.beta
                        lr_value = factor_values[2] ** self.gamma
                        fs_value = factor_values[3] ** self.phi
                        of_value = factor_values[4] ** self.omega

                        score = ti_value * as_value * lr_value * fs_value * of_value
                        self.calculated_values.append(round(score ** (1 / 5), 2))

                calculated_values_text = '\n'.join(f"{value:.2f}" for value in self.calculated_values)
                app.flow_value['-VALUES-'].update(calculated_values_text)

                mean_value = np.mean(self.calculated_values)
                app.flow_value['-MEAN-'].update(f"Общая оценка: {mean_value:.2f}")

        # Close the window
        app.close()
