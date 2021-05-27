from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse

import time
import csv
import re
import pandas as pd
from bs4 import BeautifulSoup
import random
import sql_connect
from random import randint

CHROME_DRIVER_PATH = "C://Repos//chromedriver_win32//chromedriver.exe"
chromeOptions = Options()

chromeOptions.add_argument('--kiosk')
EMAIL_REGEX = "([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
GOOGLE_URL = "https://www.google.com/"
SEARCH_TEXTS = [
    'countertop illinois',
    # 'countertop installation illinois',
    # 'countertop fabrication illinois',
]
IL_AREA_CODES = [
    '217',
    '224',
    '309',
    '312',
    '331',
    '447',
    '618',
    '630',
    '708',
    '773',
    '779',
    '815',
    '847',
    '872'
]

EXCLUDE_SITES = [
    'www.facebook.com',
    'www.hgtv.com',
    'www.homeadvisor.com'
]

FIVE_SECONDS = 5
TWO_MINUTES = 120

OUTPUT_PATH = 'output/data.csv'


class ExtractDetails:
    def __init__(self, url, email, phone, location):
        self.url = url
        self.email = email
        self.phone = phone
        self.location = location


def random_delay(min, max):
    seconds = randint(min, max)
    time.sleep(seconds)


def google_search_website(url):
    driver.get(GOOGLE_URL)

    WebDriverWait(driver, FIVE_SECONDS).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input'))
    )

    search_text = url + ' Contact'
    search_input_el = driver.find_element_by_xpath("//input[@title='Search']")
    search_input_el.send_keys(search_text)
    search_input_el.send_keys(Keys.RETURN)

    print('contact search: ' + search_text)

    WebDriverWait(driver, TWO_MINUTES).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.g a'))
    )

    link = driver.find_element_by_xpath(
        "//div[@class='g']//a").get_attribute('href')

    random_delay(1, 3)

    print('contact url ' + link)

    extract_email_from_page(link)


def extract_email_from_page(url):
    driver.get(url)

    WebDriverWait(driver, TWO_MINUTES).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'html'))
    )

    soup = BeautifulSoup(driver.page_source, "lxml")

    results = []
    for email in soup.find_all(text=re.compile(EMAIL_REGEX)):
        x = re.findall(EMAIL_REGEX, email)
        results.append(x[0])
        print('Email: ' + x[0])

    random_delay(1, 3)


def append_to_csv(data, file_name, is_header):
    # Add contents of list as last row in the csv file

    with open(file_name, 'a+', newline='') as write_obj:
        item_row = []

        for attr in dir(data):
            if attr[:2] == '__':
                continue

            if (is_header is False):
                item_row.append(getattr(data, attr))
            else:
                item_row.append(attr)

        writer = csv.writer(write_obj)
        writer.writerow(item_row)


def init_output_file():
    empty_data = ExtractDetails('Url', 'Email', 'Phone', 'Location')
    append_to_csv(empty_data, OUTPUT_PATH, True)


def is_site_valid(url):

    if url in EXCLUDE_SITES:
        return False

    existing_record = sql_connect.find_data(url)
    if existing_record is not None:
        return False

    return True


def get_website():

    index = 0
    total = 1

    while index < total:

        profiles = driver.find_elements(By.XPATH, "//div[@class='g']")
        total = len(profiles)

        current_profile = profiles[index]
        link = current_profile.find_element(
            By.XPATH, ".//a").get_attribute('href')

        link = urlparse(link).hostname

        if is_site_valid(link):
            sql_connect.insert_data("", "", "", link)

        random_delay(1, 3)
        index = index + 1

        if (index == 5):
            break


def google_search(search_text):

    driver.get(GOOGLE_URL)

    WebDriverWait(driver, FIVE_SECONDS).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input'))
    )

    search_input_el = driver.find_element_by_xpath("//input[@title='Search']")
    search_input_el.send_keys(search_text)
    search_input_el.send_keys(Keys.RETURN)

    page_num = 0
    while True:
        try:
            WebDriverWait(driver, FIVE_SECONDS).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div#search'))
            )
            page_num = page_num + 1
            print(f'On page {page_num} ' + search_text)

            get_website()

            if page_num == 2:
                break

            next_button = driver.find_element(
                By.XPATH, "//td[@role='heading']//span[text()='Next']")

            random_delay(1, 3)
            next_button.click()

        except NoSuchElementException:
            break
        except TimeoutException:
            break


def get_websites_only():
    driver = webdriver.Chrome(
        executable_path=CHROME_DRIVER_PATH, options=chromeOptions)

    # init_output_file()
    for search_text in SEARCH_TEXTS:
        google_search(search_text)


try:

    start_time = time.time()
    driver = webdriver.Chrome(
        executable_path=CHROME_DRIVER_PATH, options=chromeOptions)

    # init_output_file()
    for search_text in SEARCH_TEXTS:
        google_search(search_text)

    elapsed_time = time.time() - start_time
    print(f'TIME ELAPSED: {elapsed_time}')

finally:
    print('done')
    driver.quit()
