import csv
from random import randint
import time

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

def init_output_file(data, file_name):
    append_to_csv(data, file_name, True)

def time_delay():
    seconds = randint(5, 10)
    time.sleep(seconds)