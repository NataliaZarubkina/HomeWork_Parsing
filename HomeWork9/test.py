import pandas as pd

# Считывание исходного CSV файла
df = pd.read_csv("DisneylandReviews.csv")

# Выбор первых 40 строк
df_first_40 = df.head(40)

# Сохранение первых 40 строк в новый CSV файл
df_first_40.to_csv("DisneylandReviews.csv", index=False)