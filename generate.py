import datetime
import pandas as pd
from faker import Faker
import random

fake = Faker('ru_RU')  

# Создаем пустой DataFrame
df = pd.DataFrame(columns=['ID_Client','Имя', 'Фамилия', 'Email', 'Телефон', 'Дата'])

# Заполняем DataFrame случайными данными
data = []
i = 0
x = ['707', '777', '705', '771', '776', '700', '702', '778', '747']
y = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 
     '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 
     '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 
     '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 
     '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 
     '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
names = ['Айбек', 'Ержан', 'Аскар', 'Данияр', 'Айдар', 
             'Азамат', 'Асылхан', 'Рауан', 'Санжар', 'Бекзат', 
             'Жасулан', 'Темирлан', 'Жанболат', 'Марат', 'Бекболат', 
             'Айтуган', 'Арман', 'Доскен', 'Кайрат', 'Куаныш', 
             'Жандос', 'Абай', 'Бауржан', 'Руслан', 'Алишер',
             "Артур", "Даниил", "Максим", "Александр", "Иван",
             "Михаил", "Егор", "Никита", "Сергей", "Дмитрий",
             "Владимир", "Андрей", "Кирилл", "Антон", "Евгений",
             "Павел", "Илья", "Глеб", "Роман", "Тимофей",
             "Артем", "Игорь", "Станислав", "Владислав", "Олег"]
id_clients_data = {}  # Словарь для хранения данных клиентов по их ID

#вероятность выпадения услуг
services = [
    "Техническое_обслуживание",
    "Техническое_обслуживание",
    "Техническое_обслуживание",
    "Техническое_обслуживание",
    "Техническое_обслуживание",

    "Диагностика_двигателя",
    "Диагностика_двигателя",
    "Диагностика_двигателя",

    "Замена_масла_и_фильтров",
    "Замена_масла_и_фильтров",
    "Замена_масла_и_фильтров",

    "Ремонт_подвески",
    
    "Обслуживание_тормозной_системы",

    "Кузовной_ремонт_и_покраска",
    "Кузовной_ремонт_и_покраска",
    "Кузовной_ремонт_и_покраска",

    "Шиномонтажные_услуги",
    "Шиномонтажные_услуги",
    "Шиномонтажные_услуги",
    "Шиномонтажные_услуги",
    "Шиномонтажные_услуги",

    "Ремонт_электрических_систем",

    "Установка_и_настройка_дополнительного_оборудования"
]

#цены услуг по годам
price_2021 = {
    "Техническое_обслуживание": 3000,
    "Диагностика_двигателя" : 3000,
    "Замена_масла_и_фильтров" : 5500,
    "Ремонт_подвески" : 7000,
    "Обслуживание_тормозной_системы" : 9000,
    "Кузовной_ремонт_и_покраска": 15000,
    "Шиномонтажные_услуги": 2500,
    "Ремонт_электрических_систем":5500,
    "Установка_и_настройка_дополнительного_оборудования": 6000
}
price_2022 = {
    "Техническое_обслуживание": 4000,
    "Диагностика_двигателя" : 5000,
    "Замена_масла_и_фильтров" : 6500,
    "Ремонт_подвески" : 7000,
    "Обслуживание_тормозной_системы" : 9000,
    "Кузовной_ремонт_и_покраска": 20000,
    "Шиномонтажные_услуги": 3500,
    "Ремонт_электрических_систем":6500,
    "Установка_и_настройка_дополнительного_оборудования": 8000
}
price_2023 = {
    "Техническое_обслуживание": 5000,
    "Диагностика_двигателя" : 6000,
    "Замена_масла_и_фильтров" : 7000,
    "Ремонт_подвески" : 9000,
    "Обслуживание_тормозной_системы" : 10000,
    "Кузовной_ремонт_и_покраска": 25000,
    "Шиномонтажные_услуги": 4500,
    "Ремонт_электрических_систем":7500,
    "Установка_и_настройка_дополнительного_оборудования": 8500
}

# Заполняем DataFrame уникальными клиентами
for _ in range(905):   #905
    id_client = i + 10000
    data.append({
        'ID_Client': id_client,
        'Имя': random.choice(names),
        'Фамилия': fake.last_name_male(),
        'Email': fake.user_name() + '@gmail.com',
        'Телефон': '+7 ' + random.choice(x) + ' ' + ''.join(random.sample(y, 3)) + '-' + ''.join(random.sample(y, 4)),
        'Дата': fake.date_between(start_date=datetime.datetime(2021, 1, 1), end_date=datetime.datetime(2021, 12, 31)),
    })
    id_clients_data[id_client] = data[-1]  # Сохраняем данные клиента по его ID
    i += 1
for _ in range(1207):   #1207
    id_client = i + 10000
    data.append({
        'ID_Client': id_client,
        'Имя': random.choice(names),
        'Фамилия': fake.last_name_male(),
        'Email': fake.user_name() + '@gmail.com',
        'Телефон': '+7 ' + random.choice(x) + ' ' + ''.join(random.sample(y, 3)) + '-' + ''.join(random.sample(y, 4)),
        'Дата': fake.date_between(start_date=datetime.datetime(2022, 1, 1), end_date=datetime.datetime(2022, 12, 31)),
    })
    id_clients_data[id_client] = data[-1]  # Сохраняем данные клиента по его ID
    i += 1
for _ in range(2031):   #2031
    id_client = i + 10000
    data.append({
        'ID_Client': id_client,
        'Имя': random.choice(names),
        'Фамилия': fake.last_name_male(),
        'Email': fake.user_name() + '@gmail.com',
        'Телефон': '+7 ' + random.choice(x) + ' ' + ''.join(random.sample(y, 3)) + '-' + ''.join(random.sample(y, 4)),
        'Дата': fake.date_between(start_date=datetime.datetime(2023, 1, 1), end_date=datetime.datetime(2023, 12, 31)),
    })
    id_clients_data[id_client] = data[-1]  # Сохраняем данные клиента по его ID
    i += 1

# Заполняем DataFrame повторяющемися клиентами
for _ in range(1321):   #1321
    id_client = random.randint(10000, 14500)
    if id_client in id_clients_data:
        # Если ID уже встречался, используем сохраненные данные клиента
        data.append(id_clients_data[id_client])
    else:
        data.append({
            'ID_Client': id_client,
            'Имя': random.choice(names),
            'Фамилия': fake.last_name_male(),
            'Email': fake.user_name() + '@gmail.com',
            'Телефон': '+7 ' + random.choice(x) + ' ' + ''.join(random.sample(y, 3)) + '-' + ''.join(random.sample(y, 4)),
            'Дата': fake.date_between(start_date='-3y', end_date='-1y'),
        })
#----------------------------------------------------------------
#генерация нескольких услуг за раз
df = pd.concat([df, pd.DataFrame(data)])
spisok_yslyg = []
for _ in range(len(df)):
    i = random.randint(0, 10)
    if i > 8:
        while True:
            ser1 = random.choice(services)
            ser2 = random.choice(services)
            ser3 = random.choice(services)
            if ser1 != ser2 and ser1 != ser3 and ser2 != ser3:
                break
        service = ser1 + ' ' + ser2 + ' ' + ser3

    elif i > 6:
        while True:
            ser1 = random.choice(services)
            ser2 = random.choice(services)
            if ser1 != ser2:
                break
        service = ser1 + ' ' + ser2
    else:
        service = random.choice(services)
    spisok_yslyg.append(service)
df['Услуги'] = spisok_yslyg

df['Дата'] = pd.to_datetime(df['Дата'], errors='coerce')
#----------------------------------------------------------------

# df['Дата'] = [fake.date_between(start_date='-3y', end_date='-1y') for _ in range(len(df))]

#----------------------------------------------------------------
#генерация прогресирования
price_by_year = {
    2021: price_2021,
    2022: price_2022,
    2023: price_2023
}
def get_service_price(service, year):
    if service in price_by_year[year]:
        return price_by_year[year][service]
    else:
        return 0
df['Год'] = pd.to_datetime(df['Дата']).dt.year
df['Цена'] = df.apply(lambda row: sum([get_service_price(service, row['Год']) for service in row['Услуги'].split()]), axis=1)
df.drop(columns=['Год'], inplace=True)
#----------------------------------------------------------------

# df['Цена'] = df['Услуги'].apply(lambda x: sum([price[service] for service in x.split() if service in price]))

#----------------------------------------------------------------
#добавить отзывы случайным людям
df2 = pd.read_excel('./input_data/review.xlsx')
df2_init = df2.copy()
# df2_init.drop(columns=['с+A1:B23татус комментариев', 'СoolServis, автосервис'], inplace=True)

# Объединение данных в один датасет
merged_df = pd.concat([df, df2_init], ignore_index=True)
merged_df.to_csv('./input_data/dataset.csv', index=False)

review_indexes = list(range(len(df2_init)))
random.shuffle(review_indexes)

# Присвойте каждому клиенту отзыв
rev_ind = 0
for i, row in df.iterrows():
    # Проверяем, достаточно ли отзывов
    if rev_ind < len(review_indexes) and random.randint(0, 6) == 5:
        
        review_index = review_indexes[rev_ind]
        rev_ind += 1
        # Присваиваем клиенту отзыв из перемешанного списка
        df.at[i, 'comment'] = df2_init.at[review_index, 'comment']
        df.at[i, 'label'] = df2_init.at[review_index, 'label']
    else:
        # Если отзывов не хватает, оставляем пустое значение
        df.at[i, 'comment'] = None
        df.at[i, 'label'] = None

# Сохраните датафрейм в CSV
df.to_csv('./input_data/dataset.csv', index=False)
#----------------------------------------------------------------

# Сохраняем DataFrame в CSV
# df.to_csv('dataset.csv', index=False)
df_initial = pd.read_csv('./input_data/dataset.csv')

#----------------------------------------------------------------
# Выведем статистику по количеству различных услуг
test = " ".join(spisok_yslyg)
test = test.split(" ")
for i in set(services):
    print(i, ": ", test.count(i))

print(len(spisok_yslyg))
print(len(test))
print(df_initial['Цена'].sum())
print(df_initial[:15])
#----------------------------------------------------------------