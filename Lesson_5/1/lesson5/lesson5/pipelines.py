from pymongo import MongoClient
import csv


def process_item():
    client = MongoClient('localhost')
    db = client["test02"]
    col = db["work"]
    with open('spiders/dump.csv', 'r', encoding='utf-8') as read_obj:
        csv_reader = csv.DictReader(read_obj)
        mylist = csv_reader
        col.insert_many(mylist)


process_item()
