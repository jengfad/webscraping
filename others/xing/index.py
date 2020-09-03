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


CHROME_DRIVER_PATH = "C://Repos//chromedriver_win32//chromedriver.exe"
chromeOptions = Options()
# chromeOptions.add_argument("--headless")
# chromeOptions.add_argument('--disable-gpu')
chromeOptions.add_argument('--kiosk')
EMAIL_REGEX = "([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
GOOGLE_URL = "https://www.google.com/"
SOCSITE_URL = "https://login.xing.com/"
SOCSITE_USERNAME = 'rizwanmorin@outlook.com'
SOCSITE_PASSWORD = 'M@t@b@ng!$d@'
SEARCH_TEXT = 'site:xing.com/profile AND "executive" AND "Credit Suisse"'

FIVE_SECONDS = 5

OUTPUT_PATH = 'output/data.csv'

class PersonDetails:  
    def __init__(self, full_name, location, position): 
        self.location = location
        self.position = position

        name_parts = full_name.split()
        self.last_name = name_parts.pop()
        self.first_name = ' '.join(name_parts)

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

def extract_socsite():

    try:
        WebDriverWait(driver, FIVE_SECONDS).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div#XingIdModule"))
        )

        full_name = driver.find_element(By.XPATH, "//h1[contains(@class, 'userName')]").text
        position = driver.find_element(By.XPATH, "//div[contains(@class, 'occupationText')]/p/strong").text
        location = driver.find_element(By.XPATH, "//div[contains(@class, 'locationText')]/p").text
        
        time.sleep(1)

        details = PersonDetails(full_name, location, position)
        append_to_csv(details, OUTPUT_PATH, False)

    except Exception as e:
        print(e)
        print('NO DATA FOUND')

def get_profile_data():

    index = 0
    total = 1

    while index < total:

        profiles = driver.find_elements(By.XPATH, "//div[@class='g']")
        total = len(profiles)

        current_profile = profiles[index]
        current_profile.find_element(By.XPATH, ".//h3").click()
        extract_socsite()
        driver.execute_script("window.history.go(-1)") #go back to google page
        time.sleep(1)
        index = index + 1

        if (index == 5):
            break

def login_to_linkedin():
    driver.get(SOCSITE_URL)

    WebDriverWait(driver, FIVE_SECONDS).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input'))
    )

    driver.find_element(By.XPATH, '//input[@name="username"]').send_keys(SOCSITE_USERNAME)
    driver.find_element(By.XPATH, '//input[@name="password"]').send_keys(SOCSITE_PASSWORD)


    cookie_consent = WebDriverWait(driver, FIVE_SECONDS).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'cookie-consent')]"))
    )

    if (cookie_consent is not None):
        driver.find_element(By.XPATH, '//button[@id="consent-accept-button"]').click()
    
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()

    time.sleep(2)

def google_search():

    driver.get(GOOGLE_URL)

    WebDriverWait(driver, FIVE_SECONDS).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input'))
    )

    search_input_el = driver.find_element_by_xpath("//input[@title='Search']")
    search_input_el.send_keys(SEARCH_TEXT)
    search_input_el.send_keys(Keys.RETURN)

    while True:
        page_num = 0
        try:
            WebDriverWait(driver, FIVE_SECONDS).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div#search'))
            )
            page_num = page_num + 1
            print (f'On page {page_num}')
            get_profile_data()

            if page_num == 1:
                break

            next_button = driver.find_element(By.XPATH, "//td[@role='heading']//span[text()='Next']")

            random_timeout = random.randint(1,3)
            time.sleep(random_timeout)
            next_button.click()
    
        except NoSuchElementException:
            break
        except TimeoutException:
            break

def init_output_file():
    empty_data = PersonDetails('test', 'test', 'test')
    append_to_csv(empty_data, OUTPUT_PATH, True)

try:

    start_time = time.time()
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chromeOptions)

    init_output_file()
    login_to_linkedin()
    google_search()


    elapsed_time = time.time() - start_time
    print(f'TIME ELAPSED: {elapsed_time}')

finally:
    print('done')
    driver.quit()

