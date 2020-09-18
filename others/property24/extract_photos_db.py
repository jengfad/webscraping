
import sql_connect
import glob, os
import sql_connect
from os import listdir
from os.path import isfile, join

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

files = [f for f in listdir(PHOTOS_PATH) if isfile(join(PHOTOS_PATH, f))]
for filename in files:
    file_blob = convert_to_binary_data(filename)
    sql_connect.update_photo_blob(file_blob, filename)

# # check if blob generated is valid
# data = sql_connect.find_photo_record('110460317-1.png')
# filename = data[3]
# blob = data[4]
# write_blob_to_harddisk(blob, filename)