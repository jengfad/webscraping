from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import csv
from random import randint
from property import Property, Point_Of_Interest
import utilities

CHROME_DRIVER_PATH = "C://Repos//chromedriver_win32//chromedriver.exe"
chromeOptions = Options()
chromeOptions.add_argument("--kiosk")

driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chromeOptions)

FIVE_SECONDS = 5
MAIN_URL = 'https://www.property24.com.ph/property-for-sale?ToPrice=1500000'
OUTPUT_PATH = 'output/listing-details.csv'
POINTS_OF_INTEREST_PATH = 'output/points-of-interest.csv'
PROPERTY_DATA_PATH = 'output/property-data.csv'

def get_nullable_text(selector):
    el = driver.find_elements(By.XPATH, selector)
    if (len(el) > 0):
        return el[0].text
    else:
        return "---"

def get_nullable_bool(selector):
    el = driver.find_elements(By.XPATH, selector)
    return len(el) > 0

def get_listing_address():
    address = driver.find_elements(By.XPATH, '//div[contains(@class, "p24_listingCard p24_listingFeaturesWrapper")]/div[contains(@class, "p24_") and position() = 3]/p')
    address_fallback = driver.find_elements(By.XPATH, '//a[contains(@class, "p24_addressPropOverview")]')
    if (len(address) > 0):
        return address[0].text
    elif (len(address_fallback) > 0):
        return address_fallback[0].text
    else:
        return "---"

def click_view_more():
    for category in driver.find_elements(By.XPATH, '//div[contains(@class, "poiCategory sc_listingSummary")]'):
        view_more_button = category.find_elements(By.XPATH, './/a[contains(@class, "js_P24_viewMoreLink")]')

        if (len(view_more_button) > 0):
            view_more_button[0].click()
            time.sleep(1)
            print(f'view more button clicked...')

def get_points_of_interest(listing_number):
    panel = driver.find_elements(By.XPATH, '//div[contains(@data-target, "#accordian-points-of-interest")]')

    if (len(panel) == 0):
        return
    
    panel[0].click()
    time.sleep(1)

    click_view_more()
        
    for category in driver.find_elements(By.XPATH, '//div[contains(@class, "poiCategory sc_listingSummary")]'):
        category_name = category.find_element(By.XPATH, './/div[contains(@class, "poiCategoryName")]//h3').text

        for item in category.find_elements(By.XPATH, './/div[@class="poiItem"] | .//div[contains(@class,"poiItem js_p24_viewMoreItem")]'):
            item_name = item.find_element(By.XPATH, './/div[@class="poiItemName"]').text
            distance = item.find_element(By.XPATH, './/div[@class="poiItemDistance"]').text
            point_of_interest = Point_Of_Interest(
                listing_number,
                category_name,
                item_name,
                distance)
            utilities.append_to_csv(point_of_interest, POINTS_OF_INTEREST_PATH, False)


def get_data():
    listing_name = driver.find_element(By.XPATH, '//div[contains(@class, "sc_listingAddress")]/h1').text
    total_price = driver.find_element(By.XPATH, '//div[contains(@class, "p24_price")]').text
    listing_address = get_listing_address()
    listing_title = driver.find_element(By.XPATH, '//div[contains(@class, "p24_listingCard")]/h5').text
    listing_write_up = driver.find_element(By.XPATH, '//div[contains(@class, "sc_listingDetailsText")]').text

    bedrooms = get_nullable_text('//div[contains(@class, "p24_keyFeaturesContainer")]//div[contains(@class, "p24_listingFeatures")]//img[contains(@src, "bed")]/../../span[contains(@class, "p24_featureAmount")]')    
    bathrooms = get_nullable_text('//div[contains(@class, "p24_keyFeaturesContainer")]//div[contains(@class, "p24_listingFeatures")]//img[contains(@src, "bath")]/../../span[contains(@class, "p24_featureAmount")]')
    garages = get_nullable_text('//div[contains(@class, "p24_keyFeaturesContainer")]//div[contains(@class, "p24_listingFeatures")]//img[contains(@src, "garage")]/../../span[contains(@class, "p24_featureAmount")]')
    garden = get_nullable_bool('//div[contains(@class, "p24_keyFeaturesContainer")]//div[contains(@class, "p24_listingFeatures")]//img[contains(@src, "garden")]')
    pets_allowed = get_nullable_bool('//div[contains(@class, "p24_keyFeaturesContainer")]//div[contains(@class, "p24_listingFeatures")]//img[contains(@src, "pet")]')

    listing_number = get_nullable_text('//div[contains(@class, "p24_propertyOverviewKey") and text() = "Listing Number"]/..//div[contains(@class, "p24_info")]')
    property_type = get_nullable_text('//div[contains(@class, "p24_propertyOverviewKey") and text() = "Type of Property"]/..//div[contains(@class, "p24_info")]')
    street_address = get_nullable_text('//div[contains(@class, "p24_propertyOverviewKey") and text() = "Street Address"]/..//div[contains(@class, "p24_info")]')
    list_date = get_nullable_text('//div[contains(@class, "p24_propertyOverviewKey") and text() = "List Date"]/..//div[contains(@class, "p24_info")]')
    floor_area = get_nullable_text('//div[contains(@class, "p24_propertyOverviewKey") and text() = "Floor Area"]/..//div[contains(@class, "p24_info")]')
    lot_area = get_nullable_text('//div[contains(@class, "p24_propertyOverviewKey") and text() = "Lot Area"]/..//div[contains(@class, "p24_info")]')
    
    broker_name = "".join(driver.find_element(By.XPATH, '//div[contains(@class, "contactBottomWrap")]//div[contains(@class, "agentTitle")]').text).strip()

    data = Property(
    listing_name,
    total_price,
    listing_address,
    listing_title,
    listing_write_up,
    bedrooms,
    bathrooms,
    garages,
    garden,
    pets_allowed,
    listing_number,
    property_type,
    street_address,
    list_date,
    floor_area,
    lot_area,
    broker_name,
    url)
    utilities.append_to_csv(data, PROPERTY_DATA_PATH, False)

    get_points_of_interest(listing_number)

def init_files():
    utilities.init_output_file(Property(
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    ""), PROPERTY_DATA_PATH)
    utilities.init_output_file(Point_Of_Interest("", "", "", ""), POINTS_OF_INTEREST_PATH)

def get_property_page(property_url):

    driver.get(property_url)
    
    try:
        WebDriverWait(driver, FIVE_SECONDS).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'p24_listingCard')]"))
        )
        utilities.random_delay()
        get_data()

    except Exception as e:
        print(e)
        print('NO DATA FOUND')


try:
    urls = [
        'https://www.property24.com.ph/3-bedroom-house-and-lot-for-sale-in-quezon-city-116480188',
        # 'https://www.property24.com.ph/lot-for-sale-in-alfonso-cavite-116471156'
    ]
    start_time = time.time()
    init_files()
    for url in urls:
        get_property_page(url)

    elapsed_time = time.time() - start_time
    print(f'TIME ELAPSED: {elapsed_time}')

finally:
    print('done')
    driver.quit()