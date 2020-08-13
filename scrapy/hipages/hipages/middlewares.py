# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals, http

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


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

class HipagesSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class HipagesDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class MainPageDownloaderMiddleware:

    def process_request(self, request, spider):

        if (request.url != 'https://hipages.com.au/find/electricians/nsw/sydney'):
            return None

        url = request.url

        driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chromeOptions)
        driver.get(url)

        # load all electrician until there is no 'View More' functionality
        ctr = 1
        while True:
            try:
                element_present = EC.presence_of_element_located((By.CSS_SELECTOR, 'a[class*="view-more-sites__ViewMoreLink"]'))
                view_more_button = WebDriverWait(driver, 60).until(element_present)
                view_more_button.click()

                if (ctr == 3):
                    break
                ctr = ctr + 1

            except NoSuchElementException:
                break
            except TimeoutException:
                break

        body = driver.page_source
        driver.quit()
        return http.HtmlResponse(url=url, status=200, body=body, encoding='utf-8')

class ElectricianPageDownloaderMiddleware:
    
    def process_request(self, request, spider):

        if request.url.find('/connect/') == -1:
            return None

        url = request.url

        driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chromeOptions)
        driver.get(url)

        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class*="Header__NameBlock"] h1'))
            )
        except:
            return None
        
        shuffled_numbers = driver.find_elements_by_css_selector('span[class*="ShuffledPhoneNumber"]')
        for number in shuffled_numbers:
            number.click()

        time.sleep(0.5)

        body = driver.page_source
        driver.quit()
        return http.HtmlResponse(url=url, status=200, body=body, encoding='utf-8')
