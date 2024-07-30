#Загрузите данные который вы получили на предыдущем уроке путем скрейпинга сайта с помощью Buautiful Soup в MongoDB и создайте базу данных и коллекции для их хранения.

import json
from pymongo import MongoClient

# подключение к серверу MangoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['houston'] # выбор бзд
collection = db['housing']

with open('houston_housing market 2024_light.json', 'r') as file:
    data = json.load(file)

def changdate(data, changsize):
    for i in range(0, len(data), changsize):
        yield data[i:i + changsize]
changsize = 5000
data_chang = list(changdate(data, changsize))

for chang in data_chang:
    collection.insert_many(chang)