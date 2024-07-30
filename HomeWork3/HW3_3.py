#Загрузите данные в ClickHouse и создайте таблицу для их хранения

from clickhouse_driver import Client

client = Client(host='127.0.0.1', # Use 'localhost' or '127.0.0.1' for a local server
                user='default', # Default user, adjust if you've changed the user
                password='', # Default installation has no password for 'default' user
                port=9000) # Default TCP port for ClickHouse

# Attempt to execute a query
try:
    result = client.execute('SHOW TABLES')
    print(result)
except Exception as e:
    print(f"Encountered an error: {e}")


client.execute('SHOW TABLES')


client.execute('CREATE DATABASE IF NOT EXISTS houston')


client.execute('''
    CREATE TABLE IF NOT EXISTS houston.housing (
    id UInt64,
    address String,
    unformattedPrice Int64,
    addressCity String,
    beds Int64,
    baths Int64,
    area Int64,
    has3DModel Bool
    ) ENGINE = MergeTree()
    ORDER BY id
''')


import json


with open('houston_housing market 2024_light.json', 'r') as file:
    data = json.load(file)

# Вставка данных в таблицу
for feature in data:
    properties = feature

# Определение crash_id
hous_id = int(properties.get('id', 0))

# Вставка данных о недвижимости
client.execute("""
INSERT INTO houston.housing (
    id, address, unformattedPrice,
    addressCity, beds, baths, area, has3DModel
) VALUES""",
[(hous_id,
  properties.get('address', ''),
  properties.get('unformattedPrice', 0),
  properties.get('addressCity', ''),
  properties.get('beds', 0),
  properties.get('baths', 0),
  properties.get('area', 0),
  properties.get('has3DModel', False))
])

result = client.execute("SELECT * FROM houston.housing")
print("Inserted record:", result[0])