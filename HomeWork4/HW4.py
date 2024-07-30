import requests
from lxml import html
import pandas as pd

url = 'https://www.nbrb.by/statistics/rates/ratesDaily'
response = requests.get(url, headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})

tree = html.fromstring(response.content)

table_rows = tree.xpath("//table[@class='currencyTable']/tbody/tr")

list_data = []
for row in table_rows:
    columns = row.xpath(".//td/text()")
    list_data.append({
        'Currency': row.xpath(".//td[1]/div/span/text()")[0].strip(),
        'Multiple': columns[2].strip(),
        'Exchange_Rates': float(row.xpath(".//td[3]/div/text()")[0].strip().replace(',','.'))
        })
# print(list_data)

df = pd.DataFrame(list_data)
print(df)
df.to_csv('HomeWork4\hw_4.csv')