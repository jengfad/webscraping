# https://www.upwork.com/jobs/ASAP-Web-Scrape-Flat-Inventory-Pages-only-long-list-pages-all-info-main-list-page_~012edbf2248fd8ecc5/

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup
import time
import csv
import numpy
import pandas as pd
import json

class lot_item:  
    def __init__(self, title_name, url, customer_id, lot_number, sale_order, high_bid, quantity):  
        self.title_name = title_name  
        self.url = url
        self.customer_id = customer_id
        self.lot_number = lot_number
        self.sale_order = sale_order
        self.high_bid = high_bid
        self.quantity = quantity

CHROME_DRIVER_PATH = "C://Repos//chromedriver_win32//chromedriver.exe"
chromeOptions = Options()
chromeOptions.add_argument("--kiosk")

driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chromeOptions)

siteFilters = [
    'https://www.grafeauction.com/event/pier-1-distribution-center-groveport-day-1',
    # 'https://www.grafeauction.com/event/pier-1-distribution-center-groveport-day-2'
]

links = []
lot_dict = {}

for siteFilter in siteFilters:
    driver.get(siteFilter)

    element_present = EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class*="lot-card"]'))
    view_more_button = WebDriverWait(driver, 30).until(element_present)

    for lot_card in driver.find_elements_by_css_selector('div[class*="lot-card"]'):
        url_el = lot_card.find_element_by_css_selector('h3 a')
        url = url_el.get_attribute('href')
        title_name = url_el.text
        lot_number = lot_card.find_element_by_css_selector('span.lot-card__lot-number__value').text
        sale_order = lot_card.find_element_by_css_selector('span.lot-card__sale-order__value').text

        lot_dict[lot_number] = lot_item(title_name, url, "", lot_number, sale_order, "", "")

        # href = el.get_attribute('href')
        # links.append(href)
        # print(href)
        break


driver.quit()