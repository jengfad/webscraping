from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import csv
from random import randint
from property import Property, Point_Of_Interest, Property_Error
import utilities
import sql_connect
import urllib.request
from constants import LISTING_URLS

CHROME_DRIVER_PATH = "C://Repos//chromedriver_win32//chromedriver.exe"
chromeOptions = Options()
chromeOptions.add_argument("--kiosk")

driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chromeOptions)

FIVE_SECONDS = 5
MAIN_URL = 'https://www.property24.com.ph/property-for-sale?ToPrice=1500000'

def get_float(selector, to_replace):
    text = get_nullable_text(selector)
    if not text:
        return 0

    return float(text.replace(to_replace, "").strip())

def get_nullable_text(selector):
    el = driver.find_elements(By.XPATH, selector)
    if (len(el) > 0):
        return el[0].text
    else:
        return ""

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
        return ""

def click_view_more():
    for category in driver.find_elements(By.XPATH, '//div[contains(@class, "poiCategory sc_listingSummary")]'):
        view_more_button = category.find_elements(By.XPATH, './/a[contains(@class, "js_P24_viewMoreLink")]')

        if (len(view_more_button) > 0):
            view_more_button[0].click()
            utilities.random_delay(2, 5)

def get_points_of_interest(listing_number):
    panel = driver.find_elements(By.XPATH, '//div[contains(@data-target, "#accordian-points-of-interest")]')

    if (len(panel) == 0):
        return
    
    panel[0].click()
    utilities.random_delay(2, 5)

    click_view_more()
        
    for category in driver.find_elements(By.XPATH, '//div[contains(@class, "poiCategory sc_listingSummary")]'):
        category_name = category.find_element(By.XPATH, './/div[contains(@class, "poiCategoryName")]//h3').text

        for item in category.find_elements(By.XPATH, './/div[@class="poiItem"] | .//div[contains(@class,"poiItem js_p24_viewMoreItem")]'):
            item_name = item.find_element(By.XPATH, './/div[@class="poiItemName"]').text
            distance_km = item.find_element(By.XPATH, './/div[@class="poiItemDistance"]').text
            distance_km = float(distance_km.replace("km", "").strip())
            sql_connect.insert_interest_points(
                listing_number,
                category_name,
                item_name,
                distance_km)

def get_price(selector):
    text = get_nullable_text(selector)
    if not text:
        return 0
    
    return float(text.replace("₱ ", "").replace(",", "").strip())

def get_int(selector):
    text = get_nullable_text(selector)
    if not text:
        return 0

    return int(text)

def get_broker_name(selector):
    text = get_nullable_text(selector)
    if not text:
        return ""
    
    return text.replace("Show Email Address", "").replace("Show Contact Number", "").strip()

def get_pictures(listing_number):
    main_gallery = driver.find_elements(By.XPATH, "//div[@id='main-gallery']")
    if (len(main_gallery) == 0):
        return

    main_gallery[0].click()
    utilities.random_delay(2, 5)

    urls = []
    ctr = 1
    while True:
        src = driver.find_element(By.XPATH, '//div[@class="p24_photos"]/img')
        original_url = src.get_attribute('src')

        if (original_url in urls):
            break
        
        urls.append(original_url)
        save_dir = f'C://Repos//property-photos'
        filename = f'{listing_number}-{ctr}.jpg'
        filepath = f'{save_dir}//{filename}'
        urllib.request.urlretrieve(original_url, filepath)

        sql_connect.insert_photo_data(listing_number, original_url, filename)

        ctr = ctr + 1

        try:
            next_button = driver.find_elements(By.XPATH, '//a[contains(@class, "js_lightboxNext p24_next") and not(contains(@style, "none"))]')
            if (len(next_button) == 0):
                print('no next button...')
                break
            next_button[0].click()
            utilities.random_delay(3, 5)
        except Exception as e:
            print('Error on next button...')

def get_data():
    listing_name = get_nullable_text('//div[contains(@class, "sc_listingAddress")]/h1')
    total_price = get_price('//div[contains(@class, "p24_price")]')
    listing_address = get_listing_address()
    listing_title = get_nullable_text('//div[contains(@class, "p24_listingCard")]/h5')
    listing_write_up = get_nullable_text('//div[contains(@class, "sc_listingDetailsText")]')

    bedrooms = get_int('//div[contains(@class, "p24_keyFeaturesContainer")]//div[contains(@class, "p24_listingFeatures")]//img[contains(@src, "bed")]/../../span[contains(@class, "p24_featureAmount")]')    
    bathrooms = get_int('//div[contains(@class, "p24_keyFeaturesContainer")]//div[contains(@class, "p24_listingFeatures")]//img[contains(@src, "bath")]/../../span[contains(@class, "p24_featureAmount")]')
    garages = get_int('//div[contains(@class, "p24_keyFeaturesContainer")]//div[contains(@class, "p24_listingFeatures")]//img[contains(@src, "garage")]/../../span[contains(@class, "p24_featureAmount")]')
    garden = get_nullable_bool('//div[contains(@class, "p24_keyFeaturesContainer")]//div[contains(@class, "p24_listingFeatures")]//img[contains(@src, "garden")]')
    pets_allowed = get_nullable_bool('//div[contains(@class, "p24_keyFeaturesContainer")]//div[contains(@class, "p24_listingFeatures")]//img[contains(@src, "pet")]')

    listing_number = get_int('//div[contains(@class, "p24_propertyOverviewKey") and text() = "Listing Number"]/..//div[contains(@class, "p24_info")]')
    property_type = get_nullable_text('//div[contains(@class, "p24_propertyOverviewKey") and text() = "Type of Property"]/..//div[contains(@class, "p24_info")]')
    street_address = get_nullable_text('//div[contains(@class, "p24_propertyOverviewKey") and text() = "Street Address"]/..//div[contains(@class, "p24_info")]')
    list_date = get_nullable_text('//div[contains(@class, "p24_propertyOverviewKey") and text() = "List Date"]/..//div[contains(@class, "p24_info")]')
    floor_area_sqm = get_float('//div[contains(@class, "p24_propertyOverviewKey") and text() = "Floor Area"]/..//div[contains(@class, "p24_info")]', "SQM")
    lot_area_sqm = get_float('//div[contains(@class, "p24_propertyOverviewKey") and text() = "Lot Area"]/..//div[contains(@class, "p24_info")]', "SQM")
    
    broker_name = get_broker_name('//div[contains(@class, "contactBottomWrap")]//div[contains(@class, "agentTitle")]')

    sql_connect.insert_property_data(
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
    floor_area_sqm,
    lot_area_sqm,
    broker_name,
    url)

    get_points_of_interest(listing_number)
    get_pictures(listing_number)


def get_property_page(property_url):

    driver.get(property_url)
    
    try:
        WebDriverWait(driver, FIVE_SECONDS).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'p24_listingCard')]"))
        )
        utilities.random_delay(5, 10)
        get_data()

    except Exception as e:
        error_message = str(e)
        if hasattr(e, 'message'):
            error_message = e.message

        sql_connect.insert_error_logs(property_url, error_message)


try:
    start_time = time.time()
    for index, url in enumerate(LISTING_URLS):
        index = index + 1
        if (index == 6):
            break

        print(f'Listing #{index} of {len(LISTING_URLS)}')
        get_property_page(url)

    elapsed_time = time.time() - start_time
    print(f'TIME ELAPSED: {elapsed_time}')

finally:
    print('done')
    driver.quit()