import scrapy

html = 'https://perm.rabota.ru/'


class CatalogSpider(scrapy.Spider):
    name = 'catalog'
    start_urls = [html]

    pages_count = 10

    def start_requests(self):
        for page in range(1, 1 + self.pages_count):
            url = f'{html}?page={page}'
            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response):
        for href in response.css('h3 a::attr("href")').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        item = {
            'Вакансия': response.xpath('//h1/text()').get().strip(),
            'Зарплата': response.xpath('//h3/text()').get().replace(' ', ' '),
            'Ссылка': response.request.url,
            'Сайт': html
        }

        yield item
