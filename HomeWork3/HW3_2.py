#Поэкспериментируйте с различными методами запросов

from pymongo import MongoClient
import json

client = MongoClient()
db = client['houston']
collection = db['housing']

# вывод первой записи в коллекции
all_docs = collection.find()
first_doc = all_docs[0]


# вывод объекта json
pretty_json = json.dumps(first_doc, indent=4, default=str)
print(pretty_json)

count = collection.count_documents({})
print(f"число записей в бзд = {count}")

queru = {'hdpData.homeInfo.homeType' : 'SINGLE_FAMILY'}
print(f'Количество одноквартирных домов: {collection.count_documents(queru)}')

#- Проекция для отображения поля unformattedPrice для домов с area = 1943.
query = {'area': 1943}
proection = {'unformattedPrice': 1, '_id': 0}
project = collection.find(query, proection)
for doc in project:
    print(doc) 

query = {'unformattedPrice': {'$lt': 500000}}
print(f'Количество домов с ценой менеше 500 000$: {collection.count_documents(query)}')

query = {'unformattedPrice': {'$gte': 500000}}
print(f'Количество домов с ценой больше 500 000$: {collection.count_documents(query)}')

query = {'beds': {'$in': [1, 2]}}
print(f'Количество домов с одной или двумя спальнями: {collection.count_documents(query)}')

#- Используйте оператор $ne для подсчета количества документов, у которых "properties.rdcondition" не равно "DRY".
query = {'hdpData.homeInfo.homeType': {'$ne': 'SINGLE_FAMILY'}}
print(f'Количество многоквартирных домов: {collection.count_documents(query)}')