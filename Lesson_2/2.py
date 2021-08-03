'''
Вариант 2
Необходимо собрать информацию по продуктам питания с сайтов:
Роскачество официальный сайт. Исследование качества продуктов питания | Рейтинг товаров.
Список протестированных продуктов на сайте Росконтроль.рф
Получившийся список должен содержать:
Наименование продукта.
Категорию продукта (например «Бакалея»).
Подкатегорию продукта (например «Рис круглозерный»).
Параметр «Безопасность».
Параметр «Качество».
Общий балл.
Сайт, откуда получена информация. ### Структура должна быть одинаковая для продуктов с обоих сайтов.
Общий результат можно вывести с помощью dataFrame через Pandas.
'''

from bs4 import BeautifulSoup as bs
import requests as req
import lxml
import pandas as pd


url = 'https://roscontrol.com/'

url += 'category/produkti/'
category = url + 'category/produkti/bakaleya/'
products = url + 'category/produkti/bakaleya/krupi-i-zlakovie-hlopya/'

response = req.get(url)
soup = bs(response.text, 'lxml')
cat_products = [i.text.strip() for i in soup.find_all(class_="catalog__category-name")]

response = req.get(url + category)
soup = bs(response.text, 'lxml')
pod_cat_products = [i.text.strip() for i in soup.find_all(class_="catalog__category-name")]

response = req.get(url + products)
soup = bs(response.text, 'lxml')
krupi = [i.text.strip() for i in soup.find_all(class_="product__item-link")]
links = ['https://roscontrol.com/' + i['href'] for i in soup.find_all(class_='block-product-catalog__item')]

res_ocenki = []
for i in range(len(links)):
    response = req.get(links[i])
    soup = bs(response.text, 'lxml')
    x = soup.find(id='product__single-rev-rating').text.split()
    res_ocenki.append(f'Общая = {x[0]}, Безопасность = {x[3]}, Качество = {x[10]}')

all_res = []
for num, i in enumerate(krupi):
    all_res.append({
        'Категория': cat_products[8],
        'Подкатегория': pod_cat_products[3],
        'Наименование': i,
        'Ссылка': links[num],
        'Оценка': res_ocenki[num]
    })

for i in all_res:
    print(i)

pd.DataFrame(all_res).to_csv('dump.csv')


