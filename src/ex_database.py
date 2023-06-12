import random
import pandas as pd

random.seed(0)

# Read the CSV files
df = pd.read_csv('data/areas.csv', encoding='windows-1251')
area_list = df['area'].tolist()

df = pd.read_csv('data/years.csv', encoding='utf-8')
years_list = df['year'].astype(str).tolist()

df = pd.read_csv('data/month_year.csv', encoding='utf-8')
months_list = df['month-year'].tolist()


# df = pd.read_csv('data/full_date.csv', encoding='utf-8')
# fulldate_list = df['fulldate'].tolist()


def generate_value():
    return format(random.uniform(0.00, 1.00), ".2f")


def gen_num_val():
    return round(random.normalvariate(50000, 20000))


class DateModel:
    def __init__(self):
        # fulldate = {date: FactorsSet() for date in fulldate_list}
        months = {date: FactorsSet() for date in months_list}
        years = {date: FactorsSet() for date in years_list}
        # self.date = {**fulldate, **months, **years}
        self.date = {**months, **years}
        # self.date = years


class DatabaseModel:
    def __init__(self):
        self.area = {area: DateModel() for area in area_list}


class FactorsSet:
    def __init__(self):
        self.tourist_flow = round(random.normalvariate(100000, 20000))
        self.num_factors = {
            "Кол-во отелей": gen_num_val(),
            "Кол-во гостиниц": gen_num_val(),
            "Кол-во ресторанов": gen_num_val(),
            "Кол-во ТЦ": gen_num_val(),
            "Кол-во мед. учр.": gen_num_val(),
            "Кол-во санаториев": gen_num_val(),
            "Цена продуктов": round(random.normalvariate(15000, 5000))
        }
        self.factors = {
            "Транспортный сегмент": {
                "Публичный транспорт": generate_value(),
                "Арендованный транспорт": generate_value(),
                "Транспортная развязка": generate_value(),
                "Водный транспорт": generate_value(),
                "Подземный транспорт": generate_value(),
                "Наземный транспорт": generate_value(),
                "Такси": generate_value(),
                "Цена": generate_value()
            },
            "Сегмент размещения": {
                "Тип жилья": generate_value(),
                "Потребительская инфраструктура": generate_value(),
                "Дом": generate_value(),
                "Квартира": generate_value(),
                "Отель": generate_value(),
                "Гостиница": generate_value(),
                "Кемпинг": generate_value(),
                "Зеленая территория": generate_value(),
                "Медицинские учреждения": generate_value(),
                "Торговые центры": generate_value(),
                "Класс района": generate_value(),
                "Цена": generate_value()
            },
            "Сегмент отдыха и развлечений": {
                "Исторические ландшафты": generate_value(),
                "Природные особенности": generate_value(),
                "Спорт., муз. и др. мероприятия": generate_value(),
                "Оздоровительный отдых": generate_value(),
                "Шопинг": generate_value(),
                "Уникальные объекты": generate_value(),
                "Уникальные зоны": generate_value()
            },
            "Пищевой сегмент": {
                "Продукты": generate_value(),
                "Местные заведения": generate_value(),
                "Тип заведения": generate_value(),
                "Цена": generate_value(),
                "Разнообразие": generate_value(),
                "Национальные особенности": generate_value()
            },
            "Другие факторы": {
                "Визовые сборы": generate_value(),
                "Популярный курорт": generate_value(),
                "Природные факторы": generate_value(),
                "Количество туристов": generate_value()
            }
        }
