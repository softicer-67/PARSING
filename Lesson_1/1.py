import requests
import json


url = 'https://api.github.com'
user = 'softicer-67'


request = requests.get(f'{url}/users/{user}/repos')

js = request.json()
for i in range(0, len(js)):
    res = f'Project Number: {i + 1}\nProject Name: {js[i]["name"]}\nProject URL: {js[i]["svn_url"]}'
    print(res)

