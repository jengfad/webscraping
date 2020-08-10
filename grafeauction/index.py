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
import shutil
import requests
import os

class lot_item:  
    def __init__(self, title_name, url, customer_id, 
    lot_number, sale_order, high_bid, quantity, event_info, 
    online_premium, sales_tax, event_begins_ending, image_urls):  
        self.title_name = title_name  
        self.url = url
        self.customer_id = customer_id
        self.lot_number = lot_number
        self.sale_order = sale_order
        self.high_bid = high_bid
        self.quantity = quantity
        self.event_info = event_info
        self.online_premium = online_premium
        self.sales_tax = sales_tax
        self.event_begins_ending = event_begins_ending
        self.image_urls = image_urls

CHROME_DRIVER_PATH = "C://Repos//chromedriver_win32//chromedriver.exe"
chromeOptions = Options()
chromeOptions.add_argument("--kiosk")

driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chromeOptions)

siteFilters = [
    'https://www.grafeauction.com/event/pier-1-distribution-center-groveport-day-1',
    'https://www.grafeauction.com/event/pier-1-distribution-center-groveport-day-2'
]

links = []
lot_dict = {}

ctr = 1
for siteFilter in siteFilters:
    driver.get(siteFilter)
    element_present = EC.presence_of_element_located((By.CSS_SELECTOR, 'div.lot-card.fillbox'))
    view_more_button = WebDriverWait(driver, 30).until(element_present)

    for lot_card in driver.find_elements_by_css_selector('div.lot-card.fillbox'):
        url_el = lot_card.find_element_by_css_selector('h3 a')
        url = url_el.get_attribute('href')
        title_name = url_el.text
        lot_number = lot_card.find_element_by_css_selector('span.lot-card__lot-number__value').text
        sale_order = lot_card.find_element_by_css_selector('span.lot-card__sale-order__value').text

        lot_dict[lot_number] = lot_item(title_name, url, "", lot_number, sale_order, "", "", "", "", "", "", [])
        time.sleep(1)

        # if ctr == 10:
        #     break
        # ctr = ctr + 1

for lot_key in lot_dict:
    lot_item = lot_dict[lot_key]
    driver.get(lot_item.url)
    time.sleep(1)
    detail_el = driver.find_element_by_css_selector('div.lot-detail')
    lot_item.high_bid = detail_el.find_element_by_css_selector('span.lot-detail__high-bid__value').text
    lot_item.customer_id = detail_el.find_element_by_css_selector('span.lot-detail__high-bid__bidder').text.replace("Customer ID ", "")
    lot_item.quantity = detail_el.find_element_by_xpath('//div[contains(text(), "Qty")]').find_element_by_css_selector('strong').text
    lot_item.event_info = detail_el.find_element_by_css_selector('span.event-type').text
    lot_item.online_premium = detail_el.find_element_by_css_selector('.event-rates-online .event-rates__amount').text
    lot_item.sales_tax = detail_el.find_element_by_css_selector('.event-rates-sales-tax .event-rates__amount').text
    lot_item.event_begins_ending = detail_el.find_element_by_css_selector('.event-date--start .event-date__date').text + ' ' + detail_el.find_element_by_css_selector('.event-date--start .event-date__time').text
    images = detail_el.find_elements_by_css_selector('.carousel-item img')

    lot_item.image_urls = []
    for img in images:
        lot_item.image_urls.append(img.get_attribute('src'))

def save_image_to_file(image, dirname, suffix):
    with open('{dirname}/img_{suffix}.jpg'.format(dirname=dirname, suffix=suffix), 'wb') as out_file:
        shutil.copyfileobj(image.raw, out_file)

def download_images(dirname, links):
    length = len(links)
    for index, link in enumerate(links):
        count = index + 1
        print('Downloading image {} of {}'.format(count, length))
        response = requests.get(link, stream=True)
        save_image_to_file(response, dirname, count)
        del response

def create_directory(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

dirname = os.path.dirname(__file__)
images_dir = os.path.join(dirname, 'images')
create_directory(images_dir)

for lot_key in lot_dict:
    lot_dir = images_dir + '/Lot ' + lot_key
    create_directory(lot_dir)
    download_images(lot_dir, lot_dict[lot_key].image_urls)

output_rows = []

# build title row
title_row = []
first_item = lot_dict['1']
for attr in dir(first_item):
    if attr[:2] != '__':
        title_row.append(attr)

output_rows.append(title_row)

# build body rows
for lot_key in lot_dict:
    item_row = []
    data = lot_dict[lot_key]

    for attr in dir(data):
        if attr[:2] != '__':
            item_row.append(getattr(data,attr))

    output_rows.append(item_row)

# write to csv
f = open('draft.csv', 'w')
with f:
    writer = csv.writer(f)
    for row in output_rows:
        writer.writerow(row)

# clean up csv
df = pd.read_csv('draft.csv')
df.to_csv('output.csv', index=False)

print('Finished...')
driver.quit()