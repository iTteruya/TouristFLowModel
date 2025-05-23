import os
from crewai import Agent, Task, Crew
from crewai import LLM


ASSETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets"))

colors = [
    'b', 'g', 'c', 'y', 'k', 'orange', 'purple', 'teal',
    'navy', 'lime', 'maroon', 'olive', 'aqua', 'fuchsia', 'silver', 'gray', 'brown', 'gold',
    'darkgreen', 'orchid', 'salmon', 'plum', 'turquoise', 'indigo', 'coral', 'crimson', 'khaki', 'lavender',
    'tan', 'thistle', 'wheat', 'beige', 'chartreuse', 'chocolate', 'cornflowerblue', 'cyan', 'darkblue', 'darkcyan',
    'darkgoldenrod', 'darkgray', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darksalmon', 'darkred', 'darksagegreen', 'deepskyblue',
    'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'gainsboro', 'ghostwhite', 'greenyellow', 'honeydew', 'hotpink', 'ivory',
    'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightpink', 'lightsalmon',
    'lightseagreen', 'lightskyblue', 'lightslategray', 'lightsteelblue', 'lightyellow', 'limegreen', 'linen', 'mediumaquamarine', 'mediumblue', 'mediumorchid',
    'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin',
    'navajowhite', 'oldlace', 'olivedrab', 'orangered', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff'
]

trans_infr = ["Публичный транспорт", "Арендованный транспорт", "Транспортная развязка",
              "Водный транспорт", "Подземный транспорт", "Наземный транспорт", "Такси", "Трансфер", "Цена"]

acc_seg = ["Тип жилья", "Потребительская инфраструктура", "Дом", "Квартира", "Отель", "Гостиница",
           "Кемпинг", "Зеленая территория", "Медицинские учреждения", "Торговые центры", "Класс района", "Цена"]

food_seg = ["Исторические ландшафты", "Природные особенности", "Спорт., муз. и др. мероприятия",
            "Оздоровительный отдых", "Шопинг", "Уникальные объекты", "Уникальные зоны"]

rr = ["Продукты", "Местные заведения", "Тип заведения", "Цена", "Разнообразие", "Национальные особенности"]

other = ["Визовые сборы", "Популярный курорт", "Природные факторы", "Количество туристов"]

num_value = ["Кол-во отелей", "Кол-во гостиниц", "Кол-во ресторанов", "Кол-во ТЦ", "Кол-во мед. учр.",
             "Кол-во санаториев", "Цена продуктов"]

all_factors_by_category = {
                    "Транспортный сегмент": trans_infr,
                    "Сегмент размещения": acc_seg,
                    "Сегмент отдыха и развлечений": food_seg,
                    "Пищевой сегмент": rr,
                    "Другие факторы": other
                }

report_example = """📊 Аналитический отчет по прогнозу туристического потока в Московскую область (2015–2017)

🧩 Входные данные
Период исторических наблюдений: Февраль 2008 – Декабрь 2014

Период прогнозирования: Январь 2015 – Декабрь 2017

Тип модели: LSTM + SARIMAX с экзогенными переменными (факторы: количественные и качественные)

Метод варьирования факторов: Заданы вручную пользователем с направлением изменения (рост/снижение)

📈 Общие результаты прогноза
Прогнозируемый туристический поток в Московскую область показывает устойчивый рост на протяжении 2015–2017 годов.

Средний прирост потока составил ~6–8% ежегодно по сравнению со значениями 2014 года.

Наибольшее увеличение наблюдалось в летние месяцы, что типично для региона с умеренным климатом.

🔍 Факторы, оказавшие наибольшее влияние на рост потока
На основе анализа коэффициентов модели и динамики факторов, выделены следующие ключевые драйверы роста:

Доступность транспорта (Public Transport Availability)

📈 Увеличение числа транспортных маршрутов и улучшение их регулярности привело к росту туристического потока.

✈️ Особенно положительно повлияло расширение железнодорожных и автобусных направлений.

Цены на гостиницы (Hotel Prices)

📉 Умеренное снижение цен на отели сделало отдых более доступным.

📊 Влияние оценивается как среднеотрицательное: снижение цен сопровождалось ростом спроса.

Количество доступных гостиниц (Number of Hotels)

🏨 Рост предложения гостиничных номеров положительно повлиял на возможность принять большее количество туристов.

💡 Особенно заметен эффект в периоды пиковых нагрузок.

Индекс мероприятий и событий (Holiday Events / Marketing Score)

🎉 Проведение массовых мероприятий, фестивалей и рекламных кампаний улучшило имидж региона.

📢 Привлечён поток не только из соседних регионов, но и из отдалённых городов.

Цены на продукты питания (Average Food Prices)

🍎 Повышение цен на продовольствие имело негативное, но умеренное влияние на турпоток, особенно для семейного туризма.

✅ Рекомендации по стимулированию внутреннего туризма в Московскую область
На основе модели и анализа факторов:

1. Укрепление транспортной инфраструктуры
Продолжить субсидирование новых маршрутов и развитие мультимодальной логистики.

Внедрить единую цифровую платформу для бронирования транспорта и отелей.

2. Умеренная ценовая политика в гостиничном секторе
Поддержка малых и семейных гостиниц через льготное налогообложение и субсидии.

Разработка стандартов «доступного качества» для бюджетных туристов.

3. Организация регулярных событий и фестивалей
Создание годового календаря событий с фокусом на межсезонье.

Увеличение инвестиций в культурно-туристические кластеры и их продвижение.

4. Информационная открытость и маркетинг
Проведение рекламных кампаний в регионах с высоким потенциалом выездного туризма.

Вовлечение блогеров и цифровых платформ в продвижение уникальных особенностей региона.

5. Контроль цен и стимулирование локальной продукции
Поддержка локальных рынков и производителей для снижения ценовой нагрузки на туристов.

Развитие программ «Гастрономического туризма» с упором на местную кухню.

📌 Заключение:
Согласно прогнозу, Московская область обладает высоким потенциалом роста внутреннего туризма. Целенаправленные усилия в области инфраструктуры, ценообразования и событийного маркетинга могут существенно ускорить приток туристов и улучшить общий экономический эффект от туристической деятельности."""

def setup_forecast_analyzer_eng(forecast_data_summary: str):
    llm = LLM(model="ollama/gemma3", api_base="http://localhost:11434")

    # Define Agents
    analyst = Agent(
        role="Data Analyst",
        goal="Analyze tourist flow forecasting results and identify the most influential factors",
        backstory="You are a meticulous data scientist with expertise in time series forecasting and factor analysis. "
                  "You love digging into model results to understand what drives trends and how predictions are formed.",
        verbose=True,
        llm=llm
    )

    reporter = Agent(
        role="Tourism Journalist",
        goal="Write an insightful article summarizing the analysis of forecasted tourist flows",
        backstory="You specialize in reporting on travel and tourism trends. You want to inform decision-makers and the public "
                  "about what the data reveals, especially when it comes to changes in travel behavior and influencing factors.",
        verbose=True,
        llm=llm
    )

    # Define Tasks
    task1 = Task(
        description=(
            "Review the provided summary of forecasting results, identify which factors had the greatest impact on the forecast, "
            "discuss any trends, anomalies, or notable area differences, and explain how these insights can help improve future predictions."
        ),
        expected_output="A technical analysis of the forecasting output, key influencing factors, and data-driven recommendations.",
        agent=analyst,
        input=forecast_data_summary
    )

    task2 = Task(
        description=(
            "Using the analysis provided by the Data Analyst, write a concise but informative article suitable for a tourism industry newsletter. "
            "Highlight the key findings, implications for stakeholders (e.g., city planners, travel agencies), and possible future trends."
        ),
        expected_output="A well-written article summarizing the data analysis and its significance.",
        agent=reporter
    )

    # Create Crew
    crew = Crew(
        agents=[analyst, reporter],
        tasks=[task1, task2],
        verbose=True
    )

    result = crew.kickoff()

    # result is final text report from the Crew
    return result

def setup_forecast_analyzer_rus(forecast_data_summary: str):
    llm = LLM(model="ollama/gemma3", api_base="http://localhost:11434")

    analyst = Agent(
        role="Аналитик данных",
        goal="Проанализировать результаты прогнозирования туристических потоков и выявить наиболее влиятельные факторы",
        backstory="Вы — скрупулезный специалист по анализу данных с опытом в прогнозировании временных рядов и факторном анализе. "
                  "Вам нравится глубоко изучать результаты моделей, чтобы понять, что влияет на тренды и как формируются прогнозы.",
        verbose=True,
        llm=llm
    )

    reporter = Agent(
        role="Журналист по туризму",
        goal="Написать информативную статью, обобщающую анализ прогнозируемых туристических потоков",
        backstory="Вы специализируетесь на репортажах о тенденциях в сфере путешествий и туризма. "
                  "Вы хотите информировать заинтересованные стороны и широкую аудиторию о том, что показывает анализ данных, "
                  "особенно касательно изменений в поведении путешественников и факторов влияния.",
        verbose=True,
        llm=llm
    )

    # Определяем задачи
    task1 = Task(
        description=(
            "Изучите предоставленное резюме результатов прогнозирования, определите факторы, которые оказали наибольшее влияние на прогноз, "
            "обсудите тренды, аномалии или значимые различия между регионами, а также объясните, как эти выводы могут помочь улучшить будущие прогнозы."
        ),
        expected_output="Технический анализ результатов прогнозирования, ключевых факторов влияния и рекомендации на основе данных.",
        agent=analyst,
        input=forecast_data_summary
    )

    task2 = Task(
        description=(
            "Используя анализ, предоставленный аналитиком данных, напишите краткую, но содержательную статью, подходящую для туристической рассылки. "
            "Выделите ключевые выводы, значение для заинтересованных сторон (например, городских планировщиков, туристических агентств) и возможные будущие тенденции."
        ),
        expected_output="Хорошо написанная статья, обобщающая анализ данных и его значимость.",
        agent=reporter
    )

    crew = Crew(
        agents=[analyst, reporter],
        tasks=[task1, task2],
        verbose=True
    )

    result = crew.kickoff()
    return result