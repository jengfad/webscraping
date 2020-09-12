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