from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys

import time
import csv
import tldextract
from bs4 import BeautifulSoup
import re


CHROME_DRIVER_PATH = "C://Repos//chromedriver_win32//chromedriver.exe"
chromeOptions = Options()
chromeOptions.add_argument("--kiosk")
EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
GOOGLE_URL = "https://www.google.com/"

SCHOLARSHIP_SEARCH = [
    'scholarship',
    'career'
]

HISTORY_SEARCH = [
    'history department'
]

CREATIVE_WRITING_SEARCH = [
    'creative writing'
]

THEATER_SEARCH = [
    'theater department',
    'film department'
]

def extract_domain(url):
    if "http" in str(url) or "www" in str(url):
        parsed = tldextract.extract(url)
        parsed = ".".join([i for i in parsed if i])
        return parsed.replace('www.', '')
    else: return "NA"


def extract_email_from_page(url):
    print('navigating to search result')
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "lxml")

    results = []
    for index, email in enumerate(soup.find_all(text=re.compile(EMAIL_REGEX))):
        results.append(email)

    return results

def get_emails(school_url):  
    for search_item in HISTORY_SEARCH:
        driver.get(GOOGLE_URL)
        time.sleep(1)

        search_text = f'{school_url} {search_item}'
        search_input_el = driver.find_element_by_xpath("//input[@title='Search']")
        search_input_el.send_keys(search_text)
        search_input_el.send_keys(Keys.RETURN)
        time.sleep(1)

        link = driver.find_element_by_xpath('//div[@class="g"]//a').get_attribute('href')

        emails = extract_email_from_page(link)
        if (len(emails) > 0):
            return emails
            break
    
###########Main Function


try:
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chromeOptions)

    with open('source_files/Colleges_and_Universities.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for index, row in enumerate(csv_reader):
            if index <= 3:
                continue
            if index == 5:
                break
            
            url = row[6]
            domain = extract_domain(row[6])
            print(f'URL: {domain}')
            print(f'index is {index}')
            emails = get_emails(domain)

finally:
    driver.quit()

