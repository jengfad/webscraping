import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="password123",
  database="listings"
)

def insert_property_data(listing_name, total_price, listing_address, listing_title, listing_write_up, bedrooms, bathrooms, garages, garden, pets_allowed, listing_number, property_type, street_address, list_date, floor_area_sqm, lot_area_sqm, broker_name, url):
    mycursor = mydb.cursor()

    sql = ("INSERT INTO properties "
                "(listing_name, total_price, listing_address, listing_title, listing_write_up, bedrooms, bathrooms, garages, garden, pets_allowed, listing_number, property_type, street_address, list_date, floor_area_sqm, lot_area_sqm, broker_name, url) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    val = (listing_name, total_price, listing_address, listing_title, listing_write_up, bedrooms, bathrooms, garages, garden, pets_allowed, listing_number, property_type, street_address, list_date, floor_area_sqm, lot_area_sqm, broker_name, url)
    mycursor.execute(sql, val)

    mydb.commit()

def insert_interest_points(listing_number, category_name, item_name, distance_km):
    mycursor = mydb.cursor()

    sql = ("INSERT INTO interest_points "
                "(listing_number, category_name, item_name, distance_km) "
                "VALUES (%s, %s, %s, %s)")
    val = (listing_number, category_name, item_name, distance_km)
    mycursor.execute(sql, val)

    mydb.commit()

def insert_photo_data(listing_number, original_url, filename):
    mycursor = mydb.cursor()

    sql = ("INSERT INTO photos "
                "(listing_number, original_url, filename) "
                "VALUES (%s, %s, %s)")
    val = (listing_number, original_url, filename)
    mycursor.execute(sql, val)

    mydb.commit()

    
def insert_error_logs(notes, error_message):
    mycursor = mydb.cursor()

    sql = ("INSERT INTO error_logs "
                "(notes, error_message) "
                "VALUES (%s, %s)")
    val = (notes, error_message)
    mycursor.execute(sql, val)

    mydb.commit()

def find_photo_record(filename):
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(f"SELECT * FROM photos WHERE filename = '{filename}'")
    return mycursor.fetchone()

def get_all_photos():
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(f"SELECT * FROM photos")
    return mycursor.fetchall()

    
def find_photo_file_record(filename):
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM photo_files WHERE filename = '{filename}'")
    return mycursor.fetchone()

def insert_photo_data(listing_number, original_url, filename, file_blob):
    mycursor = mydb.cursor()

    sql = ("INSERT INTO photo_files "
                "(listing_number, original_url, filename, file) "
                "VALUES (%s, %s, %s, %s)")
    val = (listing_number, original_url, filename, file_blob)
    mycursor.execute(sql, val)

    mydb.commit()

def update_photo_blob(file, filename):
    mycursor = mydb.cursor()
    sql = """ UPDATE photos
            SET file_photo = %s
            WHERE filename = %s """
    val = (file, filename)
    mycursor.execute(sql, val)

    mydb.commit()
