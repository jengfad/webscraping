SELECT * FROM listings.photos;
SELECT * FROM listings.properties;
SELECT * FROM listings.error_logs;

DELETE FROM photos;
DELETE FROM properties;
DELETE FROM interest_points;
DELETE FROM error_logs;

USE LISTINGS;

CREATE TABLE IF NOT EXISTS error_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    notes TEXT, 
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS photos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    listing_number INT, 
    original_url TEXT, 
    filename TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS interest_points (
    id INT AUTO_INCREMENT PRIMARY KEY,
    listing_number INT, 
    category_name TEXT, 
    item_name TEXT, 
    distance_km FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS properties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    listing_name TEXT,
    total_price DOUBLE,
    listing_address TEXT,
    listing_title TEXT,
    listing_write_up LONGTEXT,
    bedrooms INT,
    bathrooms INT,
    garages INT,
    garden BOOL,
    pets_allowed BOOL,
    listing_number INT,
    property_type TEXT,
    street_address TEXT,
    list_date TEXT,
    floor_area_sqm FLOAT,
    lot_area_sqm FLOAT,
    broker_name TEXT,
    url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);