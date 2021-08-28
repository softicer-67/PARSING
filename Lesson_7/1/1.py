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

driver.get('https://passport.yandex.com/auth')  # Запускает браузер
time.sleep(1)

# Ввод логина
email_input = driver.find_element_by_id('passp-field-login')
email_input.clear()
email_input.send_keys('gbtest2021')
time.sleep(1)
click_login = driver.find_element_by_id('passp:sign-in').click()

# Ввод пароля
time.sleep(1)
pass_input = driver.find_element_by_id('passp-field-passwd')
pass_input.send_keys('333f1650')
time.sleep(1)
click_button = driver.find_element_by_id('passp:sign-in').click()
time.sleep(1)

url = 'https://mail.yandex.com/'

print('Проверка почты')
last_text = 80
post = []
for i in range(69, last_text):
    try:
        driver.get(f'https://mail.yandex.com/?uid=1474073346#message/1767662853742919{i}')
        time.sleep(2)
        send_time = driver.find_element_by_xpath('//div[5]/div[1]/div/div[2]/div[1]/div[2]/div[3]/div[1]/div[3]')
        theme = driver.find_element_by_xpath('//div[5]/div/div/div[2]/div/div/div/div/span/div')
        text = driver.find_element_by_xpath('//div[3]/div/div[5]/div[1]/div/div[3]')
        sender = driver.find_element_by_xpath('//div[5]/div[1]/div/div[2]/div[1]/div[2]/div[3]/div[1]/div[1]/span[2]/span[1]')
        time.sleep(1)
    except NoSuchElementException:
        continue

    post.append({
        'От кого': sender.text,
        'Тема письма': theme.text,
        'Время отправки': send_time.text,
        'Текст письма': text.text
    })
pd.DataFrame(post).to_csv('post.csv', mode='w', index=False)
pprint(post)


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
print('Писем больше нет')

driver.close()


