'''
2. Написать программу, которая собирает «Хиты продаж» с сайтов техники М.видео, 
ОНЛАЙН ТРЕЙД и складывает данные в БД. Магазины можно выбрать свои. 
Главный критерий выбора: динамически загружаемые товары.
'''

from selenium import webdriver
from pymongo import MongoClient
import pandas as pd
import csv
import json

driver = webdriver.Chrome('./chromedriver.exe')

url = 'https://www.onlinetrade.ru/'
driver.get(url)


all_product = []
links = []
for i in range(1, 13):
    lk = driver.find_element_by_xpath(f'/html/body/div[1]/div/div[4]/div/div[7]/div/div[2]/div[2]/div/div/div[{i}]/div[2]/div[2]/a').get_attribute('href')
    links.append(lk)

for link in links:
    driver.get(link)
    name = driver.find_element_by_xpath('//h1').text
    price = driver.find_element_by_xpath('//div[2]/div[1]/div[1]/div/span').text
    print(name)
    print(price)
    print(link)

    all_product.append({
                'Название': name,
                'Цена': price,
                'Ссылка': link
    })

pd.DataFrame(all_product).to_csv('hits.csv', index=False)

cookies = driver.get_cookies()

if cookies:
    with open('cookies.json', 'w') as o:
        json.dump(cookies, o, indent=4)

driver.close()


def to_mongo():
    client = MongoClient('localhost')
    db = client["test05"]
    col = db["HITS"]
    with open('hits.csv', 'r', encoding='utf-8') as read_obj:
        csv_reader = csv.DictReader(read_obj)
        mylist = csv_reader
        col.insert_many(mylist)


to_mongo()

