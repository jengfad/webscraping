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
chromeOptions.add_argument("--kiosk")
EMAIL_REGEX = "([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
GOOGLE_URL = "https://www.google.com/"

DEPARTMENT_DICT = {
    "history": [
        'history department',
        'creative writing',
        'arts deparment',
        'english department'
    ],
    "theater": [
        'theater department',
        'theatre department',
        'film department',
        'drama and theater arts',
        'theater and performance',
        'theater and dance'
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

def extract_domain(url):
    if "http" in str(url) or "www" in str(url):
        parsed = tldextract.extract(url)
        parsed = ".".join([i for i in parsed if i])
        return parsed.replace('www.', '')
    else: return "NA"


def extract_email_from_page(url):
    driver.get(url)

    WebDriverWait(driver, 5).until(
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
    for search_item in search_items:
        driver.get(GOOGLE_URL)

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input'))
        )

        search_text = f'{school_name} {search_item}'
        search_input_el = driver.find_element_by_xpath("//input[@title='Search']")
        search_input_el.send_keys(search_text)
        search_input_el.send_keys(Keys.RETURN)

        link = driver.find_element_by_xpath('//div[@class="g"]//a').get_attribute('href')

        emails = extract_email_from_page(link)
        if (len(emails) > 0):
            return EmailsAndLink(emails, link)
    
    # fallback
    # print('no email extracted')
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

def write_to_csv(filepath, details):
    output_rows = []

    # build title row
    title_row = []
    first_item = details[0]
    for attr in dir(first_item):
        if attr[:2] != '__':
            title_row.append(attr)

    output_rows.append(title_row)

    # build body rows
    for data in details:
        item_row = []

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
    df.to_csv(filepath, index=False)

def scrape_by_department(department_name):
    email_results = []
    with open('source_files/Colleges_and_Universities.csv', 'r') as in_file:
        csv_reader = csv.reader(in_file, delimiter=',')
        for index, row in enumerate(csv_reader, 1):


            if index <= 2:
                continue
            if index == 23:
                break
            
            index = index - 2
            print(f'Get {department_name.upper()} from School #{index}')
            
            school_name = row[0]
            url = row[6]

            if ('.com' in url):
                print('School domain contains .COM')
                continue

            extracted_emails = get_emails(school_name, DEPARTMENT_DICT[department_name])
            email_contact = get_email_result(index, school_name, url, extracted_emails)
            email_results.append(email_contact)

    for res in email_results:
        print(f'index: {res.index}, name: {res.school_name}, url: {res.school_url}, email_1: {res.email_1}, email_2: {res.email_2}')

    write_to_csv(f'output/{department_name}.csv', email_results)

try:

    start_time = time.time()
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chromeOptions)
    for department_name in DEPARTMENT_DICT:
        if (department_name != 'history'):
            continue
        scrape_by_department(department_name)

    elapsed_time = time.time() - start_time
    print(f'TIME ELAPSED: {elapsed_time}')

finally:
    print('done')
    driver.quit()

