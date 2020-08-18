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


CHROME_DRIVER_PATH = "C://Repos//chromedriver_win32//chromedriver.exe"
chromeOptions = Options()
chromeOptions.add_argument("--headless")
chromeOptions.add_argument('--disable-gpu')
EMAIL_REGEX = "([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
GOOGLE_URL = "https://www.google.com/"

TWO_MINUTES = 120

DEPARTMENT_DICT = {
    "history": [
        'history department',
        'creative writing',
        'arts deparment',
        'english department'
    ],
    "theater": [
        'theater department',
        'film department'
    ],
    "scholarship": [
        'scholarship',
        'career'
    ]
}

class EmailContact:  
    def __init__(self, index, school_name, school_url, department_link, email_1, email_2): 
        self.index = index
        self.school_name = school_name
        self.school_url = school_url
        self.department_link = department_link
        self.email_1 = email_1
        self.email_2 = email_2

class EmailsAndLink:
     def __init__(self, emails, link):
        self.emails = emails
        self.link = link


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

    # for email in re.findall(EMAIL_REGEX, driver.page_source):
    #     results.append(email)

    return results

def get_emails(school_name, search_items):

    try:

        for search_item in search_items:
            driver.get(GOOGLE_URL)

            WebDriverWait(driver, TWO_MINUTES).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input'))
            )

            search_text = f'{school_name} {search_item}'
            search_input_el = driver.find_element_by_xpath("//input[@title='Search']")
            search_input_el.send_keys(search_text)
            search_input_el.send_keys(Keys.RETURN)

            WebDriverWait(driver, TWO_MINUTES).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.r a'))
            )

            link = driver.find_element_by_xpath('//div[@class="r"]//a').get_attribute('href')

            emails = extract_email_from_page(link)
            if (len(emails) > 0):
                return EmailsAndLink(emails, link)
        
        # fallback
        # print('no email extracted')
        return EmailsAndLink([], '')

    except:
        return EmailsAndLink([], '')

###########Main Function

def get_empty_email_contact(index, school_name, school_url):
    return EmailContact(index, school_name, school_url, '', '', '')

def get_email_result(index, school_name, school_url, emails_and_link):
    item = emails_and_link
    if (len(item.emails) == 0):
        return get_empty_email_contact(index, school_name, school_url)

    if (len(item.emails) > 1):
        return EmailContact(index, school_name, school_url, item.link, item.emails[0], item.emails[1])
    else:
        return EmailContact(index, school_name, school_url, item.link, item.emails[0], '')

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


def scrape_by_department(department_name):

    output_file = f'output/{department_name}.csv'
    append_to_csv(EmailContact('', '', '', '', '', ''), output_file, True)

    with open('source_files/Colleges_and_Universities.csv', 'r') as in_file:
        csv_reader = csv.reader(in_file, delimiter=',')
        for index, row in enumerate(csv_reader, 1):


            if index <= 2:
                continue
            # if index == 6:
            #     break
            
            index = index - 2
            print(f'Get {department_name.upper()} from School #{index}')
            
            school_name = row[0]
            url = row[6]

            if ('.com' in url):
                print('School domain contains .COM')
                continue

            extracted_emails = get_emails(school_name, DEPARTMENT_DICT[department_name])
            email_contact = get_email_result(index, school_name, url, extracted_emails)
            append_to_csv(email_contact, output_file, False)


try:

    start_time = time.time()
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chromeOptions)
    for department_name in DEPARTMENT_DICT:
        if (department_name != 'scholarship'):
            continue
        scrape_by_department(department_name)

    elapsed_time = time.time() - start_time
    print(f'TIME ELAPSED: {elapsed_time}')

finally:
    print('done')
    driver.quit()

