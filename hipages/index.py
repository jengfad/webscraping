# https://www.upwork.com/job/Scrape-website-for-electrical-businesses_~010d02dc348b52c253/

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup
import time
import csv
import numpy
import pandas as pd

class detail:  
    def __init__(self, business_name, location, post_code, contact_name, phone, mobile, fax):  
        self.business_name = business_name  
        self.location = location
        self.post_code = post_code
        self.contact_name = contact_name
        self.phone = phone
        self.mobile = mobile
        self.fax = fax

CHROME_DRIVER_PATH = "C://Repos//chromedriver_win32//chromedriver.exe"
chromeOptions = Options()
chromeOptions.add_argument("--kiosk")

driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chromeOptions)

siteFilters = [
    'https://hipages.com.au/find/electricians/nsw/sydney',
    'https://hipages.com.au/find/electricians/vic/melbourne',
    'https://hipages.com.au/find/electricians/qld/brisbane',
    'https://hipages.com.au/find/electricians/wa/perth',
    'https://hipages.com.au/find/electricians/sa/adelaide'
]

links = []

for siteFilter in siteFilters:
    driver.get(siteFilter)
    time.sleep(1)

    # load all electrician until there is no 'View More' functionality
    while True:
        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, 'a[class*="view-more-sites__ViewMoreLink"]'))
            view_more_button = WebDriverWait(driver, 5).until(element_present)
            view_more_button.click()
            time.sleep(1)
        except NoSuchElementException:
            break
        except TimeoutException:
            break

    # get all links to electrician page
    for link in driver.find_elements_by_css_selector('div[class*="business-listing-header__BusinessListingHeaderColumn"] h3'):
        parent = link.find_element_by_xpath('..')
        href = parent.get_attribute('href')
        links.append(href)

def get_parent_text(soup, cssSelector):
    x = soup.select(cssSelector)
    if (len(x) == 0):
        return ""
    else:
        return x[0].parent.text

def get_contact_number(soup, cssSelector):
    x = soup.select(cssSelector)
    if len(x) == 0:
        return ""
    
    parent = x[0].parent
    return parent.select('a[class*="PhoneNumber"]')[0].text

ctr = 1
details = []
for link in links:
    driver.get(link)
    time.sleep(1)

    # electrician page not existing anymore
    if (len(driver.find_elements_by_css_selector('div[class*="Header__NameBlock"] h1')) == 0):
        continue
    
    # reveal shuffled contact numbers displayed as '...'
    shuffled_numbers = driver.find_elements_by_css_selector('span[class*="ShuffledPhoneNumber"]')
    for number in shuffled_numbers:
        number.click()

    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, "lxml")
    
    business_name = soup.select('div[class*="Header__NameBlock"] h1')[0].text
    contact_name = get_parent_text(soup, 'img[src*="contact"]')
    location = get_parent_text(soup, 'img[src*="loc"]')
    post_code = location[-4:]

    phone = get_contact_number(soup, 'img[src*="phone"]')
    mobile = get_contact_number(soup, 'img[src*="mobile"]')
    fax = get_contact_number(soup, 'img[src*="fax"]')
    details.append(detail(business_name, location, post_code, contact_name, phone, mobile, fax))

    # ctr = ctr + 1
    # if (ctr == 3):
    #     break


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
df.to_csv('output.csv', index=False)

print('Finished...')
driver.quit()


