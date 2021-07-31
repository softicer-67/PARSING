import requests
import json
import csv


url = 'https://cloud-api.yandex.net/v1/'
token = 'MDEwOlJlcG9zaXRvcnkzMzk4MzM0OTA='

headers = {
    'Content-Type': 'application/json',
    'Authorization': token
}

disk_info = 'disk'
folder_info = 'disk/resources'

res = requests.get(f'{url}{disk_info}')

print(res.json())

with open('data2.json', 'w') as f:
    writer = csv.writer(f)
    writer.writerow((res.json(),))
