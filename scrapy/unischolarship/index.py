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
EMAIL_REGEX = "([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
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

class EmailContact:  
    def __init__(self, index, school_name, school_url, email_1, email_2): 
        self.index = index
        self.school_name = school_name
        self.school_url = school_url
        self.email_1 = email_1
        self.email_2 = email_2

def extract_domain(url):
    if "http" in str(url) or "www" in str(url):
        parsed = tldextract.extract(url)
        parsed = ".".join([i for i in parsed if i])
        return parsed.replace('www.', '')
    else: return "NA"


def extract_email_from_page(url):
    print('navigating to search result')
    driver.get(url)

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'html'))
    )
    
    soup = BeautifulSoup(driver.page_source, "lxml")

    results = []
    for email in soup.find_all(text=re.compile(EMAIL_REGEX)):
        x = re.findall(EMAIL_REGEX, email)
        results.append(x[0])

    return results

def get_emails(school_name):  
    for search_item in HISTORY_SEARCH:
        driver.get(GOOGLE_URL)

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input'))
        )

        search_text = f'{search_item} {school_name}'
        search_input_el = driver.find_element_by_xpath("//input[@title='Search']")
        search_input_el.send_keys(search_text)
        search_input_el.send_keys(Keys.RETURN)

        link = driver.find_element_by_xpath('//div[@class="g"]//a').get_attribute('href')

        emails = extract_email_from_page(link)
        if (len(emails) > 0):
            return emails
    
    # fallback
    # print('no email extracted')
    return []

###########Main Function

def get_empty_email_contact(index, school_name, school_url):
    return EmailContact(index, school_name, school_url, '', '')

def get_email_result(index, school_name, school_url, emails):
    if (len(emails) == 0):
        return get_empty_email_contact(index, school_name, school_url)

    if (len(emails) > 1):
        return EmailContact(index, school_name, school_url, emails[0], emails[1])
    else:
        return EmailContact(index, school_name, school_url, emails[0], '')


try:
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chromeOptions)

        
    # emails = extract_email_from_page("http://www.sunyrockland.edu/study-at-rcc/academics-and-degrees/academic-departments/history")

    # for email in emails:
    #     print(email)

    
    email_results = []
    with open('source_files/Colleges_and_Universities.csv', 'r') as in_file:
        csv_reader = csv.reader(in_file, delimiter=',')
        for index, row in enumerate(csv_reader, 1):

            print(f'index is {index}')

            if index <= 2:
                continue
            if index == 5:
                break
            
            school_name = row[0]
            url = row[6]
            domain = extract_domain(url)

            if (domain == 'NA'):
                email_results.append(get_empty_email_contact(index, school_name, url))
                continue

            extracted_emails = get_emails(school_name)
            email_contact = get_email_result(index, school_name, url, extracted_emails)
            email_results.append(email_contact)

    for res in email_results:
        print(f'index: {res.index}, name: {res.school_name}, url: {res.school_url}, email_1: {res.email_1}, email_2: {res.email_2}')

finally:
    print('done')
    driver.quit()

