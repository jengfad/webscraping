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
chromeOptions.add_argument('--kiosk')
EMAIL_REGEX = "([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
GOOGLE_URL = "https://www.bing.com/"

WAITING_TIME = 10

OUTPUT_PATH = 'output/data.csv'

class PersonDetails:  
    def __init__(self, full_name, company, position): 
        name_parts = full_name.split()
        self.last_name = name_parts.pop()
        self.first_name = ' '.join(name_parts)
        self.company = company
        self.position = position

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

def extract_linkedin(company, position):

    try:
        WebDriverWait(driver, WAITING_TIME).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h1'))
        )

        item = driver.find_element(By.XPATH, "//div//h1")

        full_name = item.text
        print(f"{full_name}, {company}, {position}")

        time.sleep(1)

        details = PersonDetails(full_name, company, position)
        append_to_csv(details, OUTPUT_PATH, False)

    except Exception as e: # work on python 3.x
        print('Error huhu: '+ str(e))

def get_profile_data(company, position):

    profile = driver.find_element(By.XPATH, "//div[@class='b_title']//a[contains(@href,'https://au.linkedin.com/in/')]")

    if profile is None:
        return

    profile.click()
    extract_linkedin(company, position)

def google_search(company, position):
    driver.get(GOOGLE_URL)

    WebDriverWait(driver, WAITING_TIME).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea'))
    )

    search_text = f'linkedin australia {company} {position}'
    # search_text = 'site:ph.linkedin.com AND intitle:joane marie llamera'
    search_input_el = driver.find_element(By.XPATH, "//div[@class='sb_form_ic']//textarea");
    search_input_el.send_keys(search_text)
    search_input_el.send_keys(Keys.RETURN)
    time.sleep(3)

    while True:
        page_num = 0
        try:
            WebDriverWait(driver, WAITING_TIME).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div#sb_search'))
            )
            page_num = page_num + 1
            get_profile_data(company, position)

            # next_button = driver.find_element(By.XPATH, "//td[@role='heading']//span[text()='Next']")

            # random_timeout = random.randint(1,5)
            # time.sleep(random_timeout)
            # next_button.click()

            break

        except NoSuchElementException:
            break
        except TimeoutException:
            break

def read_gartner_csv():
    ctr = 0
    with open('input.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            company = row[0]
            position = row[1]

            if position.lower().find("undisclosed") == -1:
                google_search(company, position)
                ctr = ctr + 1
                print(f"On data #{ctr}")
            
        
            # if ctr == 5:
            #     break

try:

    start_time = time.time()
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chromeOptions)
    # google_search()
    read_gartner_csv()

    elapsed_time = time.time() - start_time
    print(f'TIME ELAPSED: {elapsed_time}')

finally:
    print('done')
    # driver.quit()

