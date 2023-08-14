from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys

import time
import csv
from bs4 import BeautifulSoup
import re
import pandas as pd
import random
import os

CHROME_DRIVER_PATH = "C://Repos//chromedriver_win32//chromedriver.exe"
chromeOptions = Options()
chromeOptions.add_argument('--kiosk')
chromeOptions.add_argument('--kiosk')

WAITING_TIME = 10

class CompanyDetails:  
    def __init__(self, company, business_type, website, email, linkedin, location): 
        self.company = company
        self.business_type = business_type
        self.website = website
        self.email = email
        self.linkedin = linkedin
        self.location = location

class BusinessTypeDetails:
    def __init__(self, id, type): 
        self.id = id
        self.type = type

def deleteFile(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


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

def load_all_search_results():
    SCROLL_PAUSE_TIME = 5
    last_height = get_scroll_height()
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = get_scroll_height()
        if new_height == last_height:
            break

        last_height = new_height


def get_company_details(company_link, business_type):
    driver.get(company_link)

    WebDriverWait(driver, WAITING_TIME).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div#profile'))
    )

    business_name_el = driver.find_element(By.XPATH, '//ul[@id="business-contact-details"]/li[contains(text(), "Business Name")]/following-sibling::li[1]')
    company = business_name_el.text

    business_site_el = driver.find_element(By.XPATH, '//ul[@id="business-contact-details"]/li[contains(text(), "Official Website")]/following-sibling::li[1]')
    website = business_site_el.text

    business_location_el = driver.find_element(By.XPATH, '//ul[@id="business-contact-details"]/li[contains(text(), "Business Location")]/following-sibling::li[1]')
    location = business_location_el.text

    linkedin = ''
    linkedin_selector = '//ul[@id="business-contact-details"]/li[contains(text(), "Social Links")]/following-sibling::li[1]/a[contains(@href, "linkedin")]'
    if len(driver.find_elements(By.XPATH, linkedin_selector)) > 0:
        linkedin_el = driver.find_element(By.XPATH, linkedin_selector)
        linkedin = linkedin_el.get_attribute('href')

    return CompanyDetails(company, business_type, website, '', linkedin, location)


def get_companies_by_type(type_id, type_name):
    TYPE_URL = f'https://www.purelocal.com.au/search_results?sid={type_id}'

    driver.get(TYPE_URL)

    WebDriverWait(driver, WAITING_TIME).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.catsub1'))
    )

    load_all_search_results()

    links = []
    for link in driver.find_elements(By.XPATH, "//div[@id='LazyResults']//div[contains(@class, 'hp5')]/a"):
        href = link.get_attribute('href')
        links.append(href)

    OUTPUT_PATH = f'output/{type_name}.csv'
    deleteFile(OUTPUT_PATH)

    print(len(links))

    for link in links:
        company_details = get_company_details(link, type_name)
        print(company_details)
        append_to_csv(company_details, OUTPUT_PATH, False)



def get_scroll_height():
    # Get scroll height
    height = driver.execute_script("return document.body.scrollHeight")
    return height

def get_business_types():
    SEARCH_URL = "https://www.purelocal.com.au/search";
    OUTPUT_PATH = 'output/business_types.csv'
    driver.get(SEARCH_URL)

    WebDriverWait(driver, WAITING_TIME).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'select#sid'))
    )

    deleteFile(OUTPUT_PATH)

    for option in driver.find_elements(By.XPATH, '//select[@id="sid"]/option'):
        id = option.get_attribute('value')
        type = option.text

        details = BusinessTypeDetails(id, type)
        append_to_csv(details, OUTPUT_PATH, False)

def get_data_by_business_type():
    CSV_PATH = 'output/business_types.csv'
    csv_data = pd.read_csv(CSV_PATH, header=None, names=['id','type','status'])

    for i, row in csv_data.iterrows():
        typeId = row['id']
        typeName = row['type']
        csv_data['status'] = 'done'

    csv_data.to_csv(CSV_PATH, index=False)

try:
    start_time = time.time()
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chromeOptions)
    # get_business_types()

    get_companies_by_type(140, 'Air Conditioning')

    # get_data_by_business_type()

    elapsed_time = time.time() - start_time
    print(f'TIME ELAPSED: {elapsed_time}')

finally:
    print('done')
    # driver.quit()