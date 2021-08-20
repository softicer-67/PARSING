from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from ..items import LeroyImagesItem
from urllib.parse import urljoin
from scrapy.loader.processors import MapCompose
from pymongo import MongoClient
import csv
import scrapy


class LeroySpider(CrawlSpider, scrapy.Spider):
    name = 'leroy'
    start_urls = ['https://leroymerlin.ru/offer/lakokrasochnye-materialy/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@class = 'plp-card-list__show-more']")),
        Rule(LinkExtractor(restrict_xpaths="//a[@slot = 'name']"), callback='parse_item'),
    )

    def parse_item(self, response):
        l = ItemLoader(item=LeroyImagesItem(), response=response)
        l.add_xpath('file_name', "//h1/text()[1]",
                    MapCompose(lambda i: i.replace(':', '').strip()))
        l.add_xpath('file_urls', "//uc-pdp-media-carousel/picture[1]/img/@src",
                    MapCompose(lambda i: urljoin(response.url, i)))
        l.add_xpath('price', '//uc-pdp-price-view[1]/span[1]/text()',
                    MapCompose(lambda i: i.strip().replace('[', '').replace(']', '')))

        return l.load_item()


def process_item():
    client = MongoClient('localhost')
    db = client["LEROY"]
    col = db["photo"]
    with open('../spiders/dump.csv', 'r', encoding='utf-8') as read_obj:
        csv_reader = csv.DictReader(read_obj)
        mylist = csv_reader
        col.insert_many(mylist)


process_item()
