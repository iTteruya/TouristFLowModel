import PySimpleGUI as sg

trans_infr = ["Публичный транспорт", "Арендованный транспорт", "Транспортная развязка",
              "Водный транспорт", "Подземный транспорт", "Наземный транспорт", "Такси", "Трансфер", "Цена"]
acc_seg = ["Тип жилья", "Потребительская инфраструктура", "Дом", "Квартира", "Отель", "Гостиница",
           "Кемпинг", "Зеленая территория", "Медицинские учреждения", "Торговые центры", "Класс района", "Цена"]
food_seg = ["Исторические ландшафты", "Природные особенности", "Спорт., муз. и др. мероприятия",
            "Оздоровительный отдых", "Шопинг", "Уникальные объекты", "Уникальные зоны"]
rr = ["Продукты", "Местные заведения", "Тип заведения", "Цена", "Разнообразие", "Национальные особенности"]
other = ["Визовые сборы", "Популярный курорт", "Природные факторы", "Количество туристов"]


class FactorSelector:
    def __init__(self):
        self.layout = [
            [sg.Text("Транспортный сегмент", font='Helvetica 12 bold')],
            [sg.Listbox(values=trans_infr, size=(20, 6), key="-LISTBOX1-",
                        select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, expand_x=True, expand_y=True)],
            [sg.Text("Сегмент размещения", font='Helvetica 12 bold')],
            [sg.Listbox(values=acc_seg, size=(20, 6), key="-LISTBOX2-", select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                        expand_x=True, expand_y=True)],
            [sg.Text("Сегмент отдыха и развлечений", font='Helvetica 12 bold')],
            [sg.Listbox(values=food_seg, size=(20, 6), key="-LISTBOX3-", select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                        expand_x=True, expand_y=True)],
            [sg.Text("Пищевой сегмент", font='Helvetica 12 bold')],
            [sg.Listbox(values=rr, size=(20, 6), key="-LISTBOX4-", select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                        expand_x=True, expand_y=True)],
            [sg.Text("Другие факторы", font='Helvetica 12 bold')],
            [sg.Listbox(values=other, size=(20, 6), key="-LISTBOX5-", select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                        expand_x=True, expand_y=True)],
            [sg.Button("Выход"), sg.Button("Назад"), sg.Button("Очистить"), sg.Button("Выбрать"), sg.Button("Далее")]
        ]
        self.selected_items = {
            "Транспортный сегмент": [],
            "Сегмент размещения": [],
            "Сегмент отдыха и развлечений": [],
            "Пищевой сегмент": [],
            "Другие факторы": []
        }
        self.column_layout = [
            [sg.Column(self.layout, scrollable=True, vertical_scroll_only=True, size=(370, 500))]
        ]

    def select_factors(self, app):
        # Create the window
        if app.factor_selector is None:
            app.factor_selector = sg.Window("Выбор факторов", self.column_layout, resizable=True, size=(370, 500))
            app.windows.append(app.factor_selector)
        else:
            app.factor_selector.un_hide()

        selected_window = None

        # Event loop
        while True:
            event, values = app.factor_selector.read()

            if event in (None, "Выход"):
                break

            if event == "Очистить":
                self.selected_items = {
                    "Транспортный сегмент": [],
                    "Сегмент размещения": [],
                    "Сегмент отдыха и развлечений": [],
                    "Пищевой сегмент": [],
                    "Другие факторы": []
                }
                # Clear listbox selections
                app.factor_selector["-LISTBOX1-"].Update(set_to_index=-1)
                app.factor_selector["-LISTBOX2-"].Update(set_to_index=-1)
                app.factor_selector["-LISTBOX3-"].Update(set_to_index=-1)
                app.factor_selector["-LISTBOX4-"].Update(set_to_index=-1)
                app.factor_selector["-LISTBOX5-"].Update(set_to_index=-1)

            # Save selected items when the "Выбрать" button is clicked
            elif event == "Выбрать":
                # Update the selected items dictionary
                self.selected_items["Транспортный сегмент"] = values["-LISTBOX1-"]
                self.selected_items["Сегмент размещения"] = values["-LISTBOX2-"]
                self.selected_items["Сегмент отдыха и развлечений"] = values["-LISTBOX3-"]
                self.selected_items["Пищевой сегмент"] = values["-LISTBOX4-"]
                self.selected_items["Другие факторы"] = values["-LISTBOX5-"]

                # Update selected items display
                selected_items_text = ""
                for key, values in self.selected_items.items():
                    selected_items_text += f"{key}:\n{', '.join(values)}\n\n"

                selected_window = sg.Window("Выбранные факторы",
                                            [[sg.Multiline(selected_items_text,
                                                           disabled=True, size=(40, 10), expand_x=True, expand_y=True)],
                                             [sg.Button("OK")]],
                                            resizable=True
                                            )
                while True:
                    ev, vals = selected_window.read()
                    if ev == sg.WINDOW_CLOSED or ev == "OK":
                        break
                selected_window.close()

            elif event == "Назад":
                app.factor_selector.hide()
                app.run_second_screen()

            elif event == "Далее":
                if any(values for values in self.selected_items.values()):
                    app.factor_selector.hide()

                    app.factors = self.selected_items
                    app.form_query()

                    app.run_plot_flow()
                else:
                    sg.popup("Пожалуйста, выберите хотя бы 1 фактор")

        if selected_window is not None:
            selected_window.close()

        app.close()
