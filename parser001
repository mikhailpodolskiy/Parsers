import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

data = []

for p in range(1, 2213):

    url = f"https://makitatrading.ru/brands/makita/?PAGEN_2={p}"
    r = requests.get(url)
    sleep(3)
    soup = BeautifulSoup(r.text, 'lxml')

    tovars = soup.findAll('div', class_='itemCard R2D2')

    for tovar in tovars:
        name = tovar.find('span', class_='name').text
        link = 'https://makitatrading.ru' + tovar.find('a', class_='item_title title').get('href')
        price = tovar.find('span', class_='price').get_text('|', strip=True).replace(' ', '')[:-1]
        try:
            availability = tovar.find('div', class_='availability z7_notavail').text
        except:
            availability = "NUll"
        data.append([name, link, price, availability])

print("End")
header = ['name', 'link', 'price', 'availability']
df = pd.DataFrame(data, columns=header)
df.to_csv('/Users/Mikhail/Downloads/makitatrading_prices.csv', sep=';', encoding='utf8')
