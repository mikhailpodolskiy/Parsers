import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

def download(url):
    resp = requests.get(url, stream=True)
    r = open("X:\\condeymarket\\" + url.split("/")[-1], "wb")
    for value in resp.iter_content(1024*1024):
        r.write(value)
    r.close()

url = "http://condeymarket.ru/"
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

# Получаем ссылки разделов где находятся товары в отдельный список

linkss = []
links = soup.find('ul', class_='dropdown-menu')
for i in links:
    s = 'http://condeymarket.ru' + i.find('a').get('href')
    linkss.append(s)

# Максимальное количестово страниц пагинации на отдельной странице раздела

new = []
for pp in linkss:
    url = pp
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    try:
        max_page = soup.find('p', class_='counter').get_text('|', strip=True)
        new.append(max_page.split(' ')[3])
    except:
        new.append('1')

# Все страницы разделов включая пагинацию

all_links_category = []
for number, each_link in enumerate(linkss):
    int_number = int(new[number])
    if int_number > 1:
        for pages in range(1, int_number + 1):
            all_links_category.append(each_link + f"?start={pages}0")
    else:
        all_links_category.append(each_link)


# Все страницы товаров

all_url = []

for url in all_links_category:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    all_url_pre = soup.find_all('h5', class_="item-title")
    for urlx in all_url_pre:
        z = urlx.find('a').get('href')
        all_url.append(f"http://condeymarket.ru{z}")

# Получаем данные с каждой страницы

data = []

url = 'http://condeymarket.ru/drenazhnye-pompy-dlya-kodnitsionerov/drenazhnaya-pompa-siccom-ecoline-dlya-konditsionerov-do-10-kvt'
for url in all_url:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    try:
        name = soup.find('div', class_='saleitem item-page').findAll('div', class_='page-header')[1].h1.text
    except:
        name = ""
    try:
        price = soup.find('div', class_='cost cost-rub text-right character-cost').span.get_text('|', strip=True)
    except:
        name = ""
    try:
        image = 'http://condeymarket.ru' + soup.find('div', class_='nomargin item-image').img.get('src')
        download(image) # применяем функцию для скачивания
    except:
        name = ""
    try:
        small_opisanie = soup.find('div', class_='poisition-bottom').get_text(' ', strip=True)
    except:
        name = ""
    try:
        description = soup.find('div', class_='tab-pane active').find_all('p')
    except:
        name = ""
    try:
        complect = soup.find('div', class_='tab-pane active').ul
    except:
        name = ""
    data.append([name, price, image, small_opisanie, description, complect])

# Назначаем названия столбцов

header = ['Название', 'Цена', 'Ссылка на картинку', 'Описание поставщика', 'Описание в HTML', 'Комплектация в HTML']

# Указываем что данный список будем использовать как заголовок

df = pd.DataFrame(data, columns=header)

# Настройки экспорта
df.to_csv('/Users/Mikhail/Downloads/condeymarket.csv', sep=';', encoding='utf8')
