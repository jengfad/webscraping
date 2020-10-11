
import sql_connect
import glob, os
import sql_connect
from os import listdir
from os.path import isfile, join
import urllib.request
import time

PHOTOS_PATH = "C://Repos//property-photos"

def convert_to_binary_data(filename):
    # Convert digital data to binary format
    path = f"{PHOTOS_PATH}//{filename}"
    print(path)
    with open(path, 'rb') as file:
        binaryData = file.read()
    return binaryData

def write_blob_to_harddisk(blob, filename):
    with open("C://Repos//temp//" + filename, 'wb') as file:
        file.write(blob)

def write_to_blob():
    files = [f for f in listdir(PHOTOS_PATH) if isfile(join(PHOTOS_PATH, f))]

    for index, filename in enumerate(files):
        print(f'photo #{index + 1} of {len(files)}')

    try:
        file_blob = convert_to_binary_data(filename)
        data = sql_connect.find_photo_record(filename)
        listing_number = data[1]
        original_url = data[2]
        sql_connect.insert_photo_data(listing_number, original_url, filename, file_blob)
    except Exception as e:
        print (e)

def get_from_url():
    results = sql_connect.get_all_photos()
    photos_count = len(results)
    for index, data in enumerate(results[:2]):
        try:
            listing_number = data[1]
            original_url = data[2]
            filename = data[3]
            path = f"{PHOTOS_PATH}//{filename}"
            urllib.request.urlretrieve(original_url, path)
            time.sleep(3)
        except Exception as e:
            error_message = str(e)
            if hasattr(e, 'message'):
                error_message = e.message

            sql_connect.insert_error_logs(original_url, error_message)
            print(error_message)


try:
    get_from_url()
finally:
    print('done')

# filename = '113885934-13.png'
# file_blob = convert_to_binary_data(filename)
# data = sql_connect.find_photo_record(filename)
# listing_number = data[1]
# original_url = data[2]
# sql_connect.insert_photo_data(listing_number, original_url, filename, file_blob)

# # check if blob generated is valid
# data = sql_connect.find_photo_file_record('110460317-1.png')
# filename = data[3]
# blob = data[4]
# write_blob_to_harddisk(blob, filename)

