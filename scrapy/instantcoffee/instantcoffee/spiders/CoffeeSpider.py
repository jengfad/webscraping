import scrapy


class CoffeespiderSpider(scrapy.Spider):
    name = 'CoffeeSpider'
    start_urls = ['https://www.amazon.com/']

    def parse(self, response):
        pass


