'''
1. Написать программу, которая собирает входящие письма из своего или тестового почтового ящика, 
и сложить информацию о письмах в базу данных (от кого, дата отправки, тема письма, текст письма).
'''


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
from pprint import pprint
from pymongo import MongoClient
import pandas as pd
import csv
import json


driver = webdriver.Chrome('./chromedriver.exe')

driver.get("https://passport.yandex.ru/auth")

driver.find_element_by_id("passp-field-login").clear()
driver.find_element_by_id("passp-field-login").send_keys("gbtest2021")
driver.find_element_by_id("passp:sign-in").click()
time.sleep(2)
driver.find_element_by_id("passp-field-passwd").send_keys("8732548738475")
time.sleep(2)
driver.find_element_by_id("passp:sign-in").click()
time.sleep(2)
driver.get("https://mail.yandex.ru/")

post = []


def read_post():
    send_time = driver.find_element_by_xpath('//div[5]/div[1]/div/div[2]/div[1]/div[2]/div[3]/div[1]/div[3]').text
    theme = driver.find_element_by_xpath('//div[5]/div/div/div[2]/div/div/div/div/span/div').text
    text = driver.find_element_by_xpath('//div[3]/div/div[5]/div[1]/div/div[3]').text
    sender = driver.find_element_by_xpath('//div[5]/div[1]/div/div[2]/div[1]/div[2]/div[3]/div[1]/div[1]/span[2]/span[1]').text
    post.append({
        'От кого': sender,
        'Тема письма': theme,
        'Время отправки': send_time,
        'Текст письма': text
    })
    pprint(post)
    return send_time, theme, text, sender


print('Начинаем просмотр почты...')
driver.get("https://mail.yandex.ru/?uid=1474073346#tabs/relevant")
time.sleep(3)
driver.find_element_by_xpath("//div[5]/div/div/div/div[2]/div/div/div/div/div/a/div/span/span[2]/span").click()
time.sleep(1)

for i in range(1, 20):
    print('Письмо: ', i)
    time.sleep(3)
    try:
        read_post()
        driver.find_element_by_xpath("//html[@id='nb-1']/body/div[2]/div[7]/div/div[3]/div[3]/div[3]/div/div[5]/div/div/div/div/div/a[2]/span[2]").click()
        time.sleep(2)
    except:
        break

pd.DataFrame(post).to_csv('post.csv', mode='w', index=False)


def to_mongo():
    client = MongoClient('localhost')
    db = client["test06"]
    col = db["POST"]
    with open('post.csv', 'r', encoding='utf-8') as read_obj:
        csv_reader = csv.DictReader(read_obj)
        mylist = csv_reader
        col.insert_many(mylist)


to_mongo()

print()
print('Почты больше нет в почтовом ящике...')

driver.close()
