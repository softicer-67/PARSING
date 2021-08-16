'''
Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru, yandex-новости.
Для парсинга использовать XPath. Структура данных должна содержать:
название источника;
наименование новости;
ссылку на новость;
дата публикации.
'''

from lxml import html
import requests
import datetime

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
now = datetime.datetime.now()
now = f"{'%d' % now.year}.{'%d' % now.month}.{'%d' % now.day}."
err = 'Ошибка запроса'


def request_to_mail():
    try:
        response = requests.get('https://news.mail.ru/', headers=header)
        root = html.fromstring(response.text)
        for i in range(1, 5):
            news = root.xpath(f'//*[@id="index_page"]/div[7]/div[2]/div[3]/div/div/div/div[{i}]/div/div[2]/span[2]/a/span')
            link = root.xpath(f'//*[@id="index_page"]/div[7]/div[2]/div[3]/div/div/div/div[{i}]/div/div[2]/span[2]/a/@href')
            ist = root.xpath(f'//*[@id="index_page"]/div[7]/div[2]/div[3]/div/div/div/div[{i}]/div/div[2]/div/span[2]/text()')
            tim = root.xpath(f'//*[@id="index_page"]/div[7]/div[2]/div[3]/div/div/div/div[{i}]/div/div[2]/div/span[1]')
            print([ist[0]], news[0].text, link[0], now, tim[0].text)
    except:
        print(err)


def request_to_lenta():
    try:
        url = 'https://lenta.ru/'
        response = requests.get('https://lenta.ru/', headers=header)
        root = html.fromstring(response.text)
        for i in range(5, 10):
            link = root.xpath(f'//*[@id="root"]/section[2]/div/div/div[2]/div[1]/section/div/div[{i}]/a/@href')
            news = root.xpath(f'//*[@id="root"]/section[2]/div/div/div[2]/div[1]/section/div/div[{i}]/a/text()')
            print(news[0], url + link[0], now)
    except:
        print(err)


def request_to_yandex():
    try:
        response = requests.get('https://yandex.ru/news/', headers=header)
        root = html.fromstring(response.text)
        for i in range(2, 6):
            ist = root.xpath(f'/html/body/div[3]/div/div[2]/div/div[1]/div[1]/div[{i}]/article/div[3]/div[1]/div/span[1]/a')
            link = root.xpath(f'/html/body/div[3]/div/div[2]/div/div[1]/div[1]/div[{i}]/article/div[3]/div[1]/div/span[1]/a/@href')
            news = root.xpath(f'/html/body/div[3]/div/div[2]/div/div[1]/div[1]/div[{i}]/article/div[1]/div/a/h2')
            tim = root.xpath(f'/html/body/div[3]/div/div[2]/div/div[1]/div[1]/div[{i}]/article/div[3]/div[1]/div/span[2]')
            print([ist[0].text], news[0].text, link[0], now, tim[0].text)
    except:
        print(err)


print('\tnews.mail.ru'.upper())
request_to_mail()
print('=' * 145)
print('\tlenta.ru'.upper())
request_to_lenta()
print('=' * 145)
print('\tyandex.ru/news'.upper())
request_to_yandex()
