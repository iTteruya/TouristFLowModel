import random
import psycopg2
import pandas as pd

random.seed(0)


def generate_value():
    return format(random.uniform(0.00, 1.00), ".2f")


def gen_num_val():
    return round(random.normalvariate(50000, 20000))


class DateModel:
    def __init__(self, use_db):
        if use_db:
            self.date = {}
        else:
            # Read the CSV files
            df = pd.read_csv('../data/years.csv', encoding='utf-8')
            self.years_list = df['year'].astype(str).tolist()

            df = pd.read_csv('../data/month_year.csv', encoding='utf-8')
            self.months_list = df['month-year'].tolist()

            months = {date: FactorsSet() for date in self.months_list}
            years = {date: FactorsSet() for date in self.years_list}

            """
            Warning! Generating fulldate data will take a lot of time and might freeze your PC.
            Enable at your own risk.
            """
            # df = pd.read_csv('../data/full_date.csv', encoding='utf-8')
            # self.fulldate_list = df['fulldate'].tolist()

            # fulldate = {date: FactorsSet() for date in self.fulldate_list}
            # self.date = {**fulldate, **months, **years}

            self.date = {**months, **years}
            # self.date = years

    def partial_fulldate(self, date_list):
        for date in date_list:
            if date not in self.date:
                self.date[date] = FactorsSet()



class DatabaseModel:
    def __init__(self, use_db):
        if use_db:
            self.area = {}
        else:
            # Read the CSV file
            df = pd.read_csv('../data/areas.csv', encoding='windows-1251')
            area_list = df['area'].tolist()
            self.area = {area: DateModel(use_db) for area in area_list}


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
                "Водный транспорт": generate_value(),
                "Подземный транспорт": generate_value(),
                "Наземный транспорт": generate_value(),
                "Транспортная развязка": generate_value(),
                "Трансфер": generate_value(),
                "Публичный транспорт": generate_value(),
                "Арендованный транспорт": generate_value(),
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


def setup_data(use_db):
    db_model = DatabaseModel(use_db)
    if use_db:

        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host="localhost",
            dbname="postgres",
            user="postgres",
            password=""
        )

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Query to retrieve all information
        query = """
            SELECT
                a.name AS area_name,
                f.date,
                f.tourist_flow,
                ti.water_transport,
                ti.underground_transport,
                ti.ground_transport,
                ti.transport_rent,
                ti.transfer,
                ti.public_transport,
                ti.rented_transport,
                ti.taxi,
                ti.cost,
                fs.products,
                fs.local_eating_places,
                fs.type_of_place,
                fs.cost,
                fs.variety,
                fs.national_features,
                of.visa_fees,
                of.popular_resort,
                of.natural_factors,
                of.number_tourists,
                sa.type_of_housing,
                sa.consumer_infr,
                sa.house,
                sa.apartment,
                sa.hotel,
                sa.hostel,
                sa.camping,
                sa.green_territory,
                sa.medical_institutions,
                sa.shopping_malls,
                sa.neighbourhood,
                sa.cost,
                lr.historical_landscaping,
                lr.natural_features,
                lr.events,
                lr.wellness_holiday,
                lr.shopping,
                lr.unique_objects,
                lr.unique_zones,
                nf.hotels,
                nf.hostels,
                nf.restaurants,
                nf.malls,
                nf.hospitals,
                nf.resorts,
                nf.food_price
            FROM
                factors f
                JOIN area a ON f.area_id = a.id
                JOIN transport_infrastructure ti ON f.ti_id = ti.id
                JOIN food_segment fs ON f.fs_id = fs.id
                JOIN other_factors of ON f.of_id = of.id
                JOIN segment_accommodation sa ON f.sa_id = sa.id
                JOIN leisure_and_recreation lr ON f.lr_id = lr.id
                JOIN num_factors nf ON f.nf_id = nf.id
        """

        # Execute the query
        cursor.execute(query)

        # Fetch all the rows from the result
        rows = cursor.fetchall()

        # Create the dictionary object
        data_dict = {}

        # Iterate over the rows and populate the dictionary
        for row in rows:
            area_name = row[0]
            date = row[1]
            tourist_flow = row[2]

            if area_name not in data_dict:
                data_dict[area_name] = {}

            if date not in data_dict[area_name]:
                data_dict[area_name][date] = {}

            data_dict[area_name][date]['flow'] = tourist_flow
            data_dict[area_name][date]["Транспортный сегмент"] = {
                "Водный транспорт": row[3],
                "Подземный транспорт": row[4],
                "Наземный транспорт": row[5],
                "Транспортная развязка": row[6],
                "Трансфер": row[7],
                "Публичный транспорт": row[8],
                "Арендованный транспорт": row[9],
                "Такси": row[10],
                "Цена": row[11]
            }
            data_dict[area_name][date]['Пищевой сегмент'] = {
                "Продукты": row[12],
                "Местные заведения": row[13],
                "Тип заведения": row[14],
                "Цена": row[15],
                "Разнообразие": row[16],
                "Национальные особенности": row[17]
            }
            data_dict[area_name][date]['Другие факторы'] = {
                "Визовые сборы": row[18],
                "Популярный курорт": row[19],
                "Природные факторы": row[20],
                "Количество туристов": row[21]
            }
            data_dict[area_name][date]['Сегмент размещения'] = {
                "Тип жилья": row[22],
                "Потребительская инфраструктура": row[23],
                "Дом": row[24],
                "Квартира": row[25],
                "Отель": row[26],
                "Гостиница": row[27],
                "Кемпинг": row[28],
                "Зеленая территория": row[29],
                "Медицинские учреждения": row[30],
                "Торговые центры": row[31],
                "Класс района": row[32],
                "Цена": row[33]
            }
            data_dict[area_name][date]['Сегмент отдыха и развлечений'] = {
                "Исторические ландшафты": row[34],
                "Природные особенности": row[35],
                "Спорт., муз. и др. мероприятия": row[36],
                "Оздоровительный отдых": row[37],
                "Шопинг": row[38],
                "Уникальные объекты": row[39],
                "Уникальные зоны": row[40]
            }
            data_dict[area_name][date]['Кол-во отелей'] = row[41]
            data_dict[area_name][date]['Кол-во гостиниц'] = row[42]
            data_dict[area_name][date]['Кол-во ресторанов'] = row[43]
            data_dict[area_name][date]['Кол-во ТЦ'] = row[44]
            data_dict[area_name][date]['Кол-во мед. учр.'] = row[45]
            data_dict[area_name][date]['Кол-во санаториев'] = row[46]
            data_dict[area_name][date]['Цена продуктов'] = row[47]

        # Close the cursor and database connection
        cursor.close()
        conn.close()

        # Iterate over the data_dict and populate the models
        for area_name, area_data in data_dict.items():
            if area_name not in db_model.area:
                db_model.area[area_name] = DateModel(use_db)

            for date, factors_data in area_data.items():
                if date not in db_model.area[area_name].date:
                    db_model.area[area_name].date[date] = FactorsSet()

                factors_set = db_model.area[area_name].date[date]
                factors_set.tourist_flow = factors_data['flow']
                factors_set.num_factors = {
                    "Кол-во отелей": factors_data['Кол-во отелей'],
                    "Кол-во гостиниц": factors_data['Кол-во гостиниц'],
                    "Кол-во ресторанов": factors_data['Кол-во ресторанов'],
                    "Кол-во ТЦ": factors_data['Кол-во ТЦ'],
                    "Кол-во мед. учр.": factors_data['Кол-во мед. учр.'],
                    "Кол-во санаториев": factors_data['Кол-во санаториев'],
                    "Цена продуктов": factors_data['Цена продуктов']
                }

                factors_set.factors['Транспортный сегмент'] = factors_data['Транспортный сегмент']
                factors_set.factors['Сегмент размещения'] = factors_data['Сегмент размещения']
                factors_set.factors['Сегмент отдыха и развлечений'] = factors_data['Сегмент отдыха и развлечений']
                factors_set.factors['Пищевой сегмент'] = factors_data['Пищевой сегмент']
                factors_set.factors['Другие факторы'] = factors_data['Другие факторы']

    return db_model
