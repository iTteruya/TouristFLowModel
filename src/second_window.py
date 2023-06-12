import PySimpleGUI as sg
from datetime import datetime
from dateutil.relativedelta import relativedelta


def generate_dates(start_date, end_date):
    # Determine the format based on the length of the input dates
    if len(start_date) == 10 and len(end_date) == 10:
        format = "%d-%m-%Y"
        increment = relativedelta(days=1)
    elif len(start_date) == 7 and len(end_date) == 7:
        format = "%m-%Y"
        increment = relativedelta(months=1)
    elif len(start_date) == 4 and len(end_date) == 4:
        format = "%Y"
        increment = relativedelta(years=1)
    else:
        print("Некорректный формат даты")
        return []

    # Convert string dates to datetime objects
    start = datetime.strptime(start_date, format)
    end = datetime.strptime(end_date, format)

    # Swap start and end if start is greater than end
    if start > end:
        start, end = end, start

    # Generate dates between start and end using the specified format
    current = start
    dates = []
    while current <= end:
        dates.append(current.strftime(format))
        current += increment

    return dates


class InvalidDateError(Exception):
    pass


class SecondWindow:

    def __init__(self):
        self.selected_date1 = ""
        self.selected_date2 = ""
        self.level_of_detail = None
        self.second_screen_layout = [
            [
                sg.Text("Степень детализации:"),
                sg.Radio("Год", "level_of_detail", key="-YEAR-", enable_events=True),
                sg.Radio("Месяц-Год", "level_of_detail", key="-MONTH_YEAR-", enable_events=True),
                sg.Radio("Полная дата", "level_of_detail", key="-FULL_DATE-", enable_events=True)
            ],
            [
                sg.Text("Выберите Дату 1:"),
                sg.Input(key="-DATE1-", enable_events=True, size=(20, 1), expand_x=True),
                sg.CalendarButton("Выбрать Дату 1", target="-DATE1-", format="%d-%m-%Y", disabled=True),
            ],
            [
                sg.Text("Выберите Дату 2:"),
                sg.Input(key="-DATE2-", enable_events=True, size=(20, 1), expand_x=True),
                sg.CalendarButton("Выбрать Дату 2", target="-DATE2-", format="%d-%m-%Y", disabled=True)
            ],
            [sg.Button("Выбрать Даты", key="-SAVE-")],
            [sg.Text("Выбрана Дата 1: "), sg.Text("", key="-SELECTED_DATE1-")],
            [sg.Text("Выбрана Дата 2: "), sg.Text("", key="-SELECTED_DATE2-")],
            [sg.Button("Выход"), sg.Button("Назад"), sg.Button("Далее")]
        ]
        self.set_data1 = None
        self.set_data2 = None

    def validate_date_range(self, date1, date2):
        year1 = int(date1[-4:])
        year2 = int(date2[-4:])
        if not (2000 <= year1 <= 2023) or not (2000 <= year2 <= 2023):
            raise InvalidDateError("Выбранные даты должны быть в диапазоне от 2000 до 2024 года")

    def show_second(self, app):
        # Create the window
        if app.second_window is None:
            app.second_window = sg.Window("Выбор Дат", self.second_screen_layout, resizable=True)
            app.windows.append(app.second_window)
        else:
            app.second_window.un_hide()

        # Event loop for the second window
        while True:
            second_event, second_values = app.second_window.read()
            if second_event in (None, "Выход"):
                break

            # Enable/Disable date input fields and calendar buttons based on the selected level of detail
            if second_event in ["-YEAR-", "-MONTH_YEAR-", "-FULL_DATE-"]:
                self.level_of_detail = second_event
                if self.level_of_detail == "-FULL_DATE-":
                    app.second_window["Выбрать Дату 1"].update(disabled=False)
                    app.second_window["Выбрать Дату 2"].update(disabled=False)
                if self.level_of_detail == "-MONTH_YEAR-":
                    app.second_window["Выбрать Дату 1"].update(disabled=True)
                    app.second_window["Выбрать Дату 2"].update(disabled=True)
                if self.level_of_detail == "-YEAR-":
                    app.second_window["Выбрать Дату 1"].update(disabled=True)
                    app.second_window["Выбрать Дату 2"].update(disabled=True)

            # Handle date selection
            if second_event == "-DATE1-":
                self.selected_date1 = second_values["-DATE1-"]
            elif second_event == "-DATE2-":
                self.selected_date2 = second_values["-DATE2-"]

            # Save the selected dates if "Save Dates" button is clicked
            if second_event == "-SAVE-":
                if self.level_of_detail == "-YEAR-":
                    try:
                        datetime.strptime(self.selected_date1, "%Y")
                        datetime.strptime(self.selected_date2, "%Y")
                        self.validate_date_range(self.selected_date1, self.selected_date2)
                        sg.popup(f"Выбраны даты:\nДата 1: {self.selected_date1}\nДата 2: {self.selected_date2}")
                        app.second_window["-SELECTED_DATE1-"].update(self.selected_date1)
                        app.second_window["-SELECTED_DATE2-"].update(self.selected_date2)
                        self.set_data1, self.set_data2 = self.selected_date1, self.selected_date2
                    except ValueError:
                        sg.popup("Некорректный формат даты. Пожалуйста введите дату в формате: YYYY")
                    except InvalidDateError as e:
                        sg.popup(str(e))
                elif self.level_of_detail == "-MONTH_YEAR-":
                    try:
                        datetime.strptime(self.selected_date1, "%m-%Y")
                        datetime.strptime(self.selected_date2, "%m-%Y")
                        self.validate_date_range(self.selected_date1, self.selected_date2)
                        sg.popup(f"Выбраны даты:\nДата 1: {self.selected_date1}\nДата 2: {self.selected_date2}")
                        app.second_window["-SELECTED_DATE1-"].update(self.selected_date1)
                        app.second_window["-SELECTED_DATE2-"].update(self.selected_date2)
                        self.set_data1, self.set_data2 = self.selected_date1, self.selected_date2
                    except ValueError:
                        sg.popup("Некорректный формат даты. Пожалуйста введите дату в формате: MM-YYYY")
                    except InvalidDateError as e:
                        sg.popup(str(e))
                else:
                    try:
                        datetime.strptime(self.selected_date1, "%d-%m-%Y")
                        datetime.strptime(self.selected_date2, "%d-%m-%Y")
                        self.validate_date_range(self.selected_date1, self.selected_date2)
                        sg.popup(f"Выбраны даты:\nДата 1: {self.selected_date1}\nДата 2: {self.selected_date2}")
                        app.second_window["-SELECTED_DATE1-"].update(self.selected_date1)
                        app.second_window["-SELECTED_DATE2-"].update(self.selected_date2)
                        self.set_data1, self.set_data2 = self.selected_date1, self.selected_date2
                    except ValueError:
                        sg.popup("Некорректный формат даты. Пожалуйста введите дату в формате: DD-MM-YYYY")
                    except InvalidDateError as e:
                        sg.popup(str(e))
            elif second_event == "Назад":
                app.second_window.hide()
                app.run_first_screen()
            elif second_event == "Далее":
                if self.set_data1 is not None and self.set_data2 is not None:
                    # Close the window
                    app.second_window.hide()

                    app.period = generate_dates(str(self.set_data1), str(self.set_data2))

                    app.run_factor_selector()
                else:
                    sg.popup("Пожалуйста, выберите 2 даты")
        # Close the app
        app.close()
