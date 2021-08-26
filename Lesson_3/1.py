'''
1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
записывающую собранные вакансии в созданную БД.
'''

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import csv
from pymongo import MongoClient

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}


def get_data(zp):
    resp = requests.get(f'https://www.rabota.ru/?sort=relevance&min_salary={zp}', headers=header)
    soup = bs(resp.text, 'lxml')
    result = []
    w = soup.find_all(class_="vacancy-preview-card__title")
    p = soup.find_all(class_="vacancy-preview-card__salary vacancy-preview-card__salary-blue")
    for i in range(20):
        result.append({
            'Вакансия': w[i].text.strip(),
            'Зарплата': p[i].text.strip().replace('\xa0', ' ')
        })
        print(result[i])
        pd.DataFrame(result).to_csv('dump.csv')


def to_mongo():
    client = MongoClient('localhost')
    db = client["test01"]
    col = db["work"]
    with open('dump.csv', 'r', encoding='utf-8') as read_obj:
        csv_reader = csv.DictReader(read_obj)
        mylist = csv_reader
        col.insert_many(mylist)


get_data(80000)  # Требуемая зарплата
to_mongo()






