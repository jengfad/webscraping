import scrapy, http
from scrapy.loader import ItemLoader

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

from dcasearch.items import SearchItem
from dcasearch.logger import Logger

CHROME_DRIVER_PATH = "C://Repos//chromedriver_win32//chromedriver.exe"
chromeOptions = Options()
chromeOptions.add_argument("--kiosk")

class ChirospiderSpider(scrapy.Spider):
    name = 'ChiroSpider'
    allowed_domains = ['search.dca.ca.gov']
    mainPageSearchUrl = 'http://search.dca.ca.gov/'
    start_urls = [mainPageSearchUrl]

    def parse(self, response):
        nums = [1]
        for num in nums:
            licenseNumber = str(num)
            response = self.mainPageSearch(licenseNumber)
            yield self.getDetails(response, licenseNumber)

    def getDetails(self, response, licenseNumber):
        searchItem = SearchItem()
        searchItemLoader = ItemLoader(item=searchItem, selector=response)
        Logger.log('Begin loading item')
        searchItemLoader.add_xpath('name', './/div[@class="detailContainer"]//p[@id="name"]/text()')
        searchItemLoader.add_value('licenseNumber', licenseNumber)
        searchItemLoader.add_xpath('licenseType', './/div[@class="detailContainer"]//p[@id="licType"]/text()')
        searchItemLoader.add_xpath('licenseStatus', './/div[@class="detailContainer"]//p[@id="primaryStatus"]/text()')
        searchItemLoader.add_xpath('address', './/div[@id="address"]//p[2]/text()')
        searchItemLoader.load_item()
        Logger.log('Finished loading item')
        return searchItem

    def mainPageSearch(self, licenseNumber):

        driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chromeOptions)
        driver.get(self.mainPageSearchUrl)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input#licenseNumber'))
        )

        licenseTypeDd = driver.find_element_by_xpath('//select[@id = "licenseType"]/optgroup[contains(@label, "Chiropractic Examiners")]/option[text()="Corporation"]')
        licenseTypeDd.click()
        licenseNumberInput = driver.find_element_by_xpath('//input[@id="licenseNumber"]')
        licenseNumberInput.send_keys(licenseNumber)

        searchBtn = driver.find_element_by_xpath('//input[@id="srchSubmitHome"]')
        searchBtn.click()

        time.sleep(2)
        detailsElement = ""
        try:
            newTabLink = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//a[@class="newTab"]'))
            )
            newTabLink.click()
            time.sleep(2)
            driver.switch_to.window(driver.window_handles[1])

            detailsSelector = '//div[@id="main"]'
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, detailsSelector))
            )

            detailsElement = driver.page_source

        except:
            Logger.log("No search results")

        driver.quit()
        return scrapy.http.HtmlResponse(url="", status=200, body=detailsElement, encoding='utf-8')
        
