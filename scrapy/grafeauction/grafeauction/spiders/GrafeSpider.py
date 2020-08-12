import scrapy

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class GrafespiderSpider(scrapy.Spider):
    name = 'GrafeSpider'
    allowed_domains = ['grafeauction.com']
    start_urls = ['https://www.grafeauction.com/event/pier-1-distribution-center-groveport-day-1']

    def parse(self, response):
        print('WOOT HERE')

        yield {
            'lot_number': response.xpath('//span[contains(@class, "lot-card__lot-number__value")]/text()').extract_first(),
            'sale_order': response.xpath('//span[contains(@class, "lot-card__sale-order__value")]/text()').extract_first(),
            'url': response.xpath('//h3//a/@href').extract_first()
        }


        