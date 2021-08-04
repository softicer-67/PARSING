'''
Вариант 1
Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы)
с сайтов Superjob и HH. Приложение должно анализировать несколько страниц сайта (также вводим через input
или аргументы). Получившийся список должен содержать в себе минимум:
Наименование вакансии.
Предлагаемую зарплату (отдельно минимальную и максимальную).
Ссылку на саму вакансию.
Сайт, откуда собрана вакансия. ### По желанию можно добавить ещё параметры вакансии (например, работодателя
и расположение). Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести
с помощью dataFrame через pandas.
'''

from bs4 import BeautifulSoup as bs
import requests as req
import re
import lxml
import pandas as pd

option = 'python'

http = 'https://www.superjob.ru'
url = f'https://russia.superjob.ru/vacancy/search/?keywords={option}'

respond = req.get(url)
soup = bs(respond.text, 'lxml')
vac = [i.text.strip() for i in soup.select('div a')]
lk = [i['href'] for i in soup.select('div a')]
price = [str(i.text).replace('\xa0', ' ') for i in soup.find_all(class_="_1h3Zg _2Wp8I _2rfUm _2hCDz _2ZsgW")]

vacans = []
link = []

for i in vac:
    if f'{option}' in i.lower():
        vacans.append(i)
for i in lk:
    if '/vakansii/' in i:
        link.append(http + i)


result = []
for i in range(20):
    result.append({
        'Вакансия': vacans[i],
        'Ссылка': link[i],
        'Зарплата': price[i]

    })

for i in result:
    print(i)

pd.DataFrame(result).to_csv('dump.csv')
