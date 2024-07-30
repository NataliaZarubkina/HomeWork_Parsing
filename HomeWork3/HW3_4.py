# Импорт необходимых библиотек
import pandas as pd # Импорт библиотеки pandas для работы с данными в табличном виде
from clickhouse_driver import Client # Импорт класса Client из библиотеки clickhouse_driver для работы с базой данных ClickHouse
from datetime import datetime # Импорт класса datetime из модуля datetime для работы с датами и временем

# Подключение к серверу ClickHouse
client = Client(host='127.0.0.1', # Use 'localhost' or '127.0.0.1' for a local server
                user='default', # Default user, adjust if you've changed the user
                password='', # Default installation has no password for 'default' user
                port=9000) # Default TCP port for ClickHouse
 # Создание клиента для подключения к серверу ClickHouse, работающему локально

# 1. Выполнение базового запроса для получения всех записей из таблицы 'crashes'
records = client.execute('SELECT * FROM town_cary.crashes') # Выполнение SQL-запроса к базе данных для получения всех записей из таблицы 'crashes'
df_records = pd.DataFrame(records, columns=['id', 'location_description', 'rdfeature', 'rdsurface', 'rdcondition', 'lightcond', 'weather', 'crash_date', 'year', 'fatalities', 'injuries', 'month']) # Преобразование полученных записей в DataFrame с указанием названий столбцов
df_records.head() # Вывод первых пяти записей DataFrame для предварительного просмотра
