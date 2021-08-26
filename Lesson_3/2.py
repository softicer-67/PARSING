'''
2. Написать функцию, которая производит поиск и выводит на экран вакансии
с заработной платой больше введённой суммы.
'''

import requests
from bs4 import BeautifulSoup as bs

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}


def get_data(zp):
    resp = requests.get(f'https://www.rabota.ru/?sort=relevance&min_salary={zp}', headers=header)
    soup = bs(resp.text, 'lxml')
    work = []
    price = []
    result = []
    for i in range(20):
        w = soup.find_all(class_="vacancy-preview-card__title")
        work.append(w[i].text.strip())
        p = soup.find_all(class_="vacancy-preview-card__salary vacancy-preview-card__salary-blue")
        price.append(p[i].text.strip().replace('\xa0', ' '))

        result.append({
            'Вакансия': work[i],
            'Зарплата': price[i]
        })

        print(result[i])


get_data(80000)
