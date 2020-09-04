import scrapy
from transit.items import TransitItem

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

CHROME_DRIVER_PATH = "C://Repos//chromedriver_win32//chromedriver.exe"
chromeOptions = Options()
chromeOptions.add_argument("--kiosk")

class CaTransitSpiderSpider(scrapy.Spider):
    name = 'ca_transit_spider'
    allowed_domains = ['home.cc.umanitoba.ca']
    fn = 'https://home.cc.umanitoba.ca/~wyatt/alltime'
    # start_urls = ['https://home.cc.umanitoba.ca/~wyatt/alltime/operators.html']
    start_urls = ['https://home.cc.umanitoba.ca/~wyatt/alltime/localities.html']
    main_url = 'https://home.cc.umanitoba.ca/~wyatt/alltime/index.html'
    crawled_urls = []

    def get_prefixed_url(self, href):
        return f'{self.fn}/{href}'

    def get_province_urls(self):
        driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chromeOptions)
        driver.get(self.main_url)

        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'h1'))
            )
        except:
            return None

        urls = []
        for url in driver.find_elements_by_xpath('//table[position()=1]//a'):
            urls.append(url.get_attribute('href'))

        driver.quit()
        return urls

    def start_requests(self):
        urls = self.get_province_urls()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_province_page)

    def parse_province_page(self, response):
        for index, href in enumerate(response.xpath('//table[position() = 1]//a/@href').getall()):
            url = self.get_prefixed_url(href)
            yield scrapy.Request(url=url, callback=self.parse_history_page)

    def parse(self, response):

        # test = response.xpath('//table[position()=1]//a/@href').get()
        # print('test')
        # print(test)

        for index, href in enumerate(response.xpath('//ol//a/@href').getall()):


            # if index == 2:
            #     break

            # href = 'vancouver-bc.html'

            # if '#' in href:
            #     part_index = href.index('#')
            #     page_part = href[part_index:len(href)]
            #     href = href.replace(page_part, '')

            url = self.get_prefixed_url(href)

            
            print(f'operator #{index}: {url}')

            # if (url in self.crawled_urls):
            #     print('already crawled ' + url)
            #     continue

            self.crawled_urls.append(url)
            yield scrapy.Request(url=url, callback=self.parse_history_page)

    def parse_history_page(self, response):
        for index, header in enumerate(response.xpath('//b')):
            
            print(f'header #{index}')

            date = "".join(header.xpath('./text()').getall()).strip()

            if 'PRESENT' not in date.upper():
                continue

            link = header.xpath('.//a')
            
            if link:
                name = "".join(link.xpath('.//i/text()').get()).strip()
            else:
                name = header.xpath('.//i[1]/text()').get()
                if not name:
                    name = name = header.xpath('.//..//i[1]/text()').get()

            transit_item = TransitItem()
            transit_item['name'] = name
            transit_item['date'] = date.strip().replace('(', '').replace(')', '')
            transit_item['url'] = response.url

            yield transit_item