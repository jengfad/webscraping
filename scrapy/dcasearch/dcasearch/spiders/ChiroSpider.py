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

    hard_stop = 2
    last_valid_license_number = ""

    def parse(self, response):
        nums = [20, 5000, 5001, 5002, 5003]
        invalid_ctr = 0
        for num in nums:
        # for num, x in enumerate(range(2), 1):
            license_number = str(num)
            response = self.mainPageSearch(license_number)
            details = self.getDetails(response, license_number)

            if not details.get("main_name"):
                invalid_ctr = invalid_ctr + 1
            else:
                invalid_ctr = 0
                self.last_valid_license_number = license_number

            if (invalid_ctr > self.hard_stop):
                Logger.log('Hardstop on License %s' %(license_number))
                self.write_last_valid_license()
                break

            yield details

    def write_last_valid_license(self):
        path = 'output/ChiroCorporation/Last Number.txt'
        with open(path, 'w') as out_file:
             out_file.write(self.last_valid_license_number)
            

    def getDetails(self, response, licenseNumber):
        search_item = SearchItem()
        search_item_loader = ItemLoader(item=search_item, selector=response)
        Logger.log('Begin loading item')

        search_item_loader.add_xpath('main_name', './/header//div[@class="detailContainer"]//p[@id="name"]/text()')
        search_item_loader.add_value('main_license_number', licenseNumber)
        search_item_loader.add_xpath('main_license_type', './/header//div[@class="detailContainer"]//p[@id="licType"]/text()')
        search_item_loader.add_xpath('main_license_status', './/header//div[@class="detailContainer"]//p[@id="primaryStatus"]/text()')
        search_item_loader.add_xpath('main_address', './/header//div[@id="address"]//p[2]/text()')
        
        search_item_loader.add_xpath('relation_name', './/div[@class="relDetailPad"]//span[@class="relDetailHeader" and contains(text(), "Name")]/parent::p/text()')
        search_item_loader.add_xpath('relation_license_number', './/div[@class="relDetailPad"]//a[@class="newTab"]/text()')
        search_item_loader.add_xpath('relation_license_status', '//div[@class="relDetailPad"]//span[@class="relDetailHeader" and contains(text(), "Status")]/following-sibling::text()')
        search_item_loader.add_xpath('relation_license_type', './/div[@class="relDetailPad"]//span[@class="relDetailHeader" and contains(text(), "Type")]/parent::p/text()')
        search_item_loader.add_xpath('relation_address', './/div[@class="relDetailPad" and @id="address"]//p[1]/text()')

        search_item_loader.load_item()
        Logger.log('Finished loading item')
        return search_item

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
        
