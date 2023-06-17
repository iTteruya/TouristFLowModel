import PySimpleGUI as sg
import pandas as pd


class FirstWindow:

    def __init__(self):
        # Read the CSV file
        df = pd.read_csv('../data/areas.csv', encoding='windows-1251')
        self.area_list = df['area'].tolist()
        # Selected countries
        self.selected_areas = set()
        # Next screen trigger
        self.sec_scr_trigger = False

        # Define the layout of the GUI
        self.first_screen_layout = [
            [sg.Text("Выберите регионы", font=("Helvetica", 16))],
            [sg.InputText(key="-SEARCH-", size=(30, 1), enable_events=True, expand_x=True)],
            [sg.Listbox(values=self.area_list, size=(40, 10), select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED,
                        key="-COUNTRIES-", enable_events=True, bind_return_key=True, expand_x=True, expand_y=True)],
            [sg.Button("Выход"), sg.Button("Очистить"), sg.Button("Выбрать"), sg.Button("Далее")]
        ]

    def show_first(self, app):
        # Create the windows
        if app.first_window is None:
            app.first_window = sg.Window("Выберите регионы", self.first_screen_layout,
                                         resizable=True, size=(450, 350))
            app.windows.append(app.first_window)
        else:
            app.first_window.un_hide()
        # Event loop
        while True:
            event, values = app.first_window.read()
            if event in (None, "Выход"):
                break
            elif event == "-SEARCH-":
                search_term = values["-SEARCH-"].strip().lower()
                filtered_countries = [country for country in self.area_list if search_term in country.lower()]
                app.first_window["-COUNTRIES-"].update(values=filtered_countries)
                app.first_window["-COUNTRIES-"].set_value(list(self.selected_areas))
            elif event == "-COUNTRIES-":
                clicked_countries = values["-COUNTRIES-"]
                for country in clicked_countries:
                    if country not in self.selected_areas:
                        self.selected_areas.add(country)
                    else:
                        self.selected_areas.remove(country)
                        if len(self.selected_areas) == 0:
                            self.sec_scr_trigger = False
                app.first_window["-COUNTRIES-"].update(
                    set_to_index=[i for i, country in enumerate(self.area_list) if
                                  country in self.selected_areas])
            elif event == "Выбрать":
                selected_countries_text = "\n".join(self.selected_areas)
                sg.popup("Выбранные регионы:", selected_countries_text)
                if len(self.selected_areas) > 0:
                    self.sec_scr_trigger = True
            elif event == "Очистить":
                self.selected_areas = set()
                self.sec_scr_trigger = False
            elif event == "Далее":
                if self.sec_scr_trigger:
                    # Close the first window
                    app.first_window.hide()

                    app.areas = self.selected_areas

                    app.run_second_screen()
                else:
                    sg.popup("Пожалуйста, выберите хотя бы 1 регион")

        # Close the window
        app.close()
