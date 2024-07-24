import requests
from bs4 import BeautifulSoup
import json

# Функция для получения информации о книгах на странице
def scrape_books(url, soup):
    books = []
    
    for book in soup.find_all('article', class_='product_pod'):
        title = book.h3.a['title']
        
        # Очистка цены от лишних символов и преобразование в число
        price_text = book.find('p', class_='price_color').get_text().strip()
        price = float(price_text.replace('Â£', '').replace(',', ''))
        
        availability = book.find('p', class_='instock availability').get_text().strip()
        
        if availability == "In stock":
            books.append({
                'title': title,
                'price': price
            })
        
    return books

# URL сайта для скрапинга
url = 'http://books.toscrape.com/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

all_books = []

# Получение информации о книгах на всех страницах
while True:
    books_data = scrape_books(url, soup)
    all_books.extend(books_data)
    
    next_page = soup.find('li', class_='next')
    if not next_page:
        break
    
    url = url + next_page.a['href']
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

# Сохранение информации в JSON файл
with open('books_data.json', 'w') as f:
    json.dump(all_books, f, indent=4)

print("Данные успешно сохранены в books_data.json")