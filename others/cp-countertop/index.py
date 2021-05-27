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
    # 'countertop illinois',
    'countertop installation illinois',
    'countertop fabrication illinois',
]

IL_ZIPCODE = '604'
IL_ABBR = 'IL'

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
    'www.homeadvisor.com',
    'en.wikipedia.org',
    'www.homedepot.com',
    'www.linkedin.com',
    'www.nytimes.com',
    'www.pinterest.com',
    'www.yelp.com'
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


def extract_email():
    soup = BeautifulSoup(driver.page_source, "lxml")

    results = ''
    for email in soup.find_all(text=re.compile(EMAIL_REGEX)):
        x = re.findall(EMAIL_REGEX, email)
        item = x[0].lower()
        if item not in results:
            results = results + ', ' + item

    # has email/s
    if results:
        return results[2:len(results)]

    return results


def element_exists_by_xpath(selector):
    try:
        driver.find_element(By.XPATH, selector)
    except NoSuchElementException:
        return False
    return True


def extract_location():

    selectorAbbr = f".//*[contains(text(),'IL 6')]"
    selectorFull = f".//*[contains(text(),'Illinois')]"

    if element_exists_by_xpath(selectorAbbr):
        location = driver.find_element(By.XPATH, selectorAbbr).text
        return location

    if element_exists_by_xpath(selectorFull):
        location = driver.find_element(By.XPATH, selectorFull).text
        return location

    return ''


def extract_phone():

    for code in IL_AREA_CODES:
        selector = f".//*[contains(text(),'{code}')]"

        if element_exists_by_xpath(selector):
            phone = driver.find_element(By.XPATH, selector).text
            return phone

    return ""


def extract_details_from_page(contact_url, website):
    driver.get(contact_url)

    WebDriverWait(driver, TWO_MINUTES).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'html'))
    )

    phone = extract_phone()
    location = extract_location()
    email = extract_email()

    sql_connect.update_data(website, email, location, phone)

    random_delay(1, 3)


def is_site_valid(url):

    if url in EXCLUDE_SITES:
        return False

    existing_record = sql_connect.find_data(url)
    if existing_record is not None:
        return False

    return True


def get_contact_website(website):
    driver.get(GOOGLE_URL)

    WebDriverWait(driver, FIVE_SECONDS).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input'))
    )

    search_text = website + ' contact'

    search_input_el = driver.find_element_by_xpath("//input[@title='Search']")
    search_input_el.send_keys(search_text)
    search_input_el.send_keys(Keys.RETURN)

    WebDriverWait(driver, TWO_MINUTES).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.g a'))
    )

    link = driver.find_element_by_xpath(
        '//div[@class="g"]//a').get_attribute('href')

    extract_details_from_page(link, website)


def test_update():
    sql_connect.update_data('www.yelp.com', 'test@email.com',
                            'Illinois', '902-202-1233')


def update_website_data():
    results = sql_connect.get_all_data()
    count = len(results)
    for index, data in enumerate(results):
        website = data[4]
        get_contact_website(website)
        print(f'extracted {index} of {count}')


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

        # if (index == 5):
        #     break


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

            # if page_num == 2:
            #     break

            next_button = driver.find_element(
                By.XPATH, "//td[@role='heading']//span[text()='Next']")

            random_delay(1, 3)
            next_button.click()

        except NoSuchElementException:
            break
        except TimeoutException:
            break


try:

    start_time = time.time()
    driver = webdriver.Chrome(
        executable_path=CHROME_DRIVER_PATH, options=chromeOptions)

    # DO NOT RUN STEP 1 AND 2 AT THE SAME TIME

    # STEP1 - Extract website links first
    # for search_text in SEARCH_TEXTS:
    #     google_search(search_text)

    # STEP2 - Extract website details
    update_website_data()

    elapsed_time = time.time() - start_time
    print(f'TIME ELAPSED: {elapsed_time}')

finally:
    print('done')
    driver.quit()
