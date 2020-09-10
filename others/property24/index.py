from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import csv
import pandas as pd
from random import randint

CHROME_DRIVER_PATH = "C://Repos//chromedriver_win32//chromedriver.exe"
chromeOptions = Options()
chromeOptions.add_argument("--kiosk")

driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chromeOptions)

FIVE_SECONDS = 5
MAIN_URL = 'https://www.property24.com.ph/property-for-sale?ToPrice=1500000'
OUTPUT_PATH = 'output/data.csv'

class Listing:  
    def __init__(self, listing_url, page_url):
        self.listing_url = listing_url
        self.page_url = page_url

def append_to_csv(data, file_name, is_header):
    # Add contents of list as last row in the csv file
    
    with open(file_name, 'a+', newline='') as write_obj:
        item_row = []

        for attr in dir(data):
            if attr[:2] == '__':
                continue

            if (is_header is False):
                item_row.append(getattr(data,attr))
            else:
                item_row.append(attr)

        writer = csv.writer(write_obj)
        writer.writerow(item_row)

def time_delay():
    seconds = randint(5, 10)
    time.sleep(seconds)

def get_listings(page_url):

    driver.get(page_url)
    
    try:
        WebDriverWait(driver, FIVE_SECONDS).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.sc_panelWrapper"))
        )
        time_delay()

        for link in driver.find_elements(By.XPATH, '//div[contains(@class, "sc_listingTile")]//div[contains(@class, "sc_listingTileContent")]/a[1]'):
            listing_url = link.get_attribute('href')
            data = Listing(listing_url, page_url)
            append_to_csv(data, OUTPUT_PATH, False)

    except Exception as e:
        print(e)
        print('NO DATA FOUND')

        
try:
    start_time = time.time()
    for num in range(5):
        page_num = num + 1
        print(f'page number {page_num}')
        page_url = f'{MAIN_URL}&Page={page_num}'
        get_listings(page_url)

    elapsed_time = time.time() - start_time
    print(f'TIME ELAPSED: {elapsed_time}')

finally:
    print('done')
    driver.quit()