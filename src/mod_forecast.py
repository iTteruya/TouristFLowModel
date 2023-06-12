import PySimpleGUI as sg

trans_infr = ["Публичный транспорт", "Арендованный транспорт", "Транспортная развязка",
              "Водный транспорт", "Подземный транспорт", "Наземный транспорт", "Такси", "Цена", "Общая оценка"]
acc_seg = ["Тип жилья", "Потребительская инфраструктура", "Дом", "Квартира", "Отель", "Гостиница",
           "Кемпинг", "Зеленая территория", "Медицинские учреждения", "Торговые центры",
           "Класс района", "Цена", "Общая оценка"]
food_seg = ["Исторические ландшафты", "Природные особенности", "Спорт., муз. и др. мероприятия",
            "Оздоровительный отдых", "Шопинг", "Уникальные объекты", "Уникальные зоны", "Общая оценка"]
rr = ["Продукты", "Местные заведения", "Тип заведения", "Цена", "Разнообразие",
      "Национальные особенности", "Общая оценка"]
other = ["Визовые сборы", "Популярный курорт", "Природные факторы", "Количество туристов", "Общая оценка"]
num_value = ["Кол-во отелей", "Кол-во гостиниц", "Кол-во ресторанов", "Кол-во ТЦ", "Кол-во мед. учр.",
             "Кол-во санаториев", "Цена продуктов"]

all_factors = [trans_infr, acc_seg, food_seg, rr, other, num_value]
names_of = ["Транспортный сегмент", "Сегмент размещения", "Пищевой сегмент",
            "Сегмент отдыха и развлечений", "Другие факторы", "Количественные факторы"]

# Define the list of parameters and their initial values
parameters = []

for i, section in enumerate(names_of):
    for j, name in enumerate(all_factors[i]):
        parameter = {
            'section': section,
            'name': name,
            'value': None,
            'use_checkbox': True,
            'delta_value': None,
            'options': ['Up', 'Down', 'Mix'],
            'selected_option': 'Up'
        }
        parameters.append(parameter)


class SetupForecast:
    def __init__(self):
        # Create the layout
        self.layout = [
            [sg.Text('Количество шагов:'), sg.Input(key='num_steps', size=(10, 1))],
            [sg.Button('Выбрать все'), sg.Button('Снять все')],
            [sg.HorizontalSeparator()]
        ]

        self.checkbox_elements = []
        self.input_elements = []
        self.combo_elements = []
        self.delta_input_elements = []
        self.selected_items = {}
        self.steps = None

        current_section = None

        for i, parameter in enumerate(parameters):
            section = parameter['section']
            name = parameter['name']
            value = parameter['value']
            use_checkbox = parameter['use_checkbox']
            delta_value = parameter['delta_value']
            options = parameter['options']
            selected_option = parameter['selected_option']

            if section != current_section:
                current_section = section
                self.layout.append([sg.Text(section, font='Helvetica 12 bold')])

            checkbox = sg.Checkbox('', default=use_checkbox, key=f'use_{i}', enable_events=True)
            self.checkbox_elements.append(checkbox)

            input_element = sg.Input(default_text='' if value is None else str(value), key=name, size=(10, 1),
                                     disabled=not use_checkbox)
            self.input_elements.append(input_element)

            combo_element = sg.Combo(options, default_value=selected_option, key=f'option_{i}',
                                     disabled=not use_checkbox)
            self.combo_elements.append(combo_element)

            delta_input_element = sg.Input(default_text='' if delta_value is None else str(delta_value),
                                           key=f'delta_{i}',
                                           disabled=not use_checkbox, size=(10, 1))
            self.delta_input_elements.append(delta_input_element)

            self.layout.append([
                checkbox,
                sg.Text(f'{name}', size=(25, 1)),
                sg.Text('| Value:', size=(5, 1)),
                input_element,
                sg.Text('Delta:', size=(4, 1)),
                delta_input_element,
                sg.Text('Option:', size=(5, 1)),
                combo_element
            ])

        self.layout.append([sg.Button('Выход'), sg.Button('Назад'), sg.Button('Выбрать'), sg.Button('Далее')])
        # Wrap the layout in a Column element
        self.column_layout = [
            [sg.Column(self.layout, scrollable=True, vertical_scroll_only=True)]
        ]

    def show_setup(self, app):
        # Create the window
        if app.setup is None:
            # Create the window
            app.setup = sg.Window('Parameter Viewer', self.column_layout, resizable=True)
            app.windows.append(app.setup)
        else:
            app.setup.un_hide()
        # Event loop
        while True:
            event, values = app.setup.read()

            if event == sg.WINDOW_CLOSED or event == 'Выход':
                break

            if event.startswith('use_'):
                checkbox_index = int(event.split('_')[1])
                checkbox_value = values[event]
                input_element = self.input_elements[checkbox_index]
                combo_element = self.combo_elements[checkbox_index]
                delta_input_element = self.delta_input_elements[checkbox_index]
                input_element.update(disabled=not checkbox_value)
                combo_element.update(disabled=not checkbox_value)
                delta_input_element.update(disabled=not checkbox_value)

            if event == 'Выбрать все':
                for checkbox, input_element, combo_element, delta_input_element in zip(
                        self.checkbox_elements,
                        self.input_elements,
                        self.combo_elements,
                        self.delta_input_elements
                ):
                    checkbox.update(value=True)
                    input_element.update(disabled=False)
                    combo_element.update(disabled=False)
                    delta_input_element.update(disabled=False)

            if event == 'Снять все':
                for checkbox, input_element, combo_element, delta_input_element in zip(
                        self.checkbox_elements,
                        self.input_elements,
                        self.combo_elements,
                        self.delta_input_elements
                ):
                    checkbox.update(value=False)
                    input_element.update(disabled=True)
                    combo_element.update(disabled=True)
                    delta_input_element.update(disabled=True)

            if event == "Назад":
                app.setup.hide()
                app.run_plot_flow()

            if event == "Далее":
                if self.selected_items:
                    app.setup.hide()
                    app.run_forecast()
                else:
                    sg.popup("Пожалуйста, выберите хотя бы 1 параметр")

            if event == 'Выбрать':
                has_invalid_input = False  # Flag to track invalid input
                updated_parameters = []
                self.selected_items = {}
                for parameter, checkbox, input_element, \
                    combo_element, delta_input_element in zip(parameters,
                                                              self.checkbox_elements,
                                                              self.input_elements,
                                                              self.combo_elements,
                                                              self.delta_input_elements):
                    name = parameter['name']
                    use_checkbox = checkbox.get()
                    value = input_element.get()
                    delta_value = delta_input_element.get()
                    selected_option = combo_element.get()

                    if use_checkbox:
                        try:
                            value = float(value)
                            delta_value = float(delta_value)
                            parameter['value'] = value
                            parameter['delta_value'] = delta_value
                            parameter['selected_option'] = selected_option
                            updated_parameters.append(parameter)
                            self.selected_items[name] = {
                                'value': value,
                                'delta_value': delta_value,
                                'selected_option': selected_option
                            }
                        except ValueError:
                            has_invalid_input = True  # Invalid input encountered
                    else:
                        parameter['value'] = None
                        parameter['delta_value'] = None
                        parameter['selected_option'] = None
                        updated_parameters.append(parameter)

                num_steps = values['num_steps']
                try:
                    num_steps = int(num_steps)
                except ValueError:
                    has_invalid_input = True  # Invalid input encountered

                if has_invalid_input:
                    sg.popup('Неверный ввод. Пожалуйста введите числовые значения для всех выбранных полей.')

                    # Perform further processing only if there were no invalid inputs
                if not has_invalid_input:
                    # Perform any further processing with the updated parameters and num_steps
                    # For example, print the updated parameters and num_steps
                    app.steps = num_steps
                    print(f'Selected Items: {self.selected_items}')
                    print(f'Number of Steps: {num_steps}')

        # Close the window
        app.close()
