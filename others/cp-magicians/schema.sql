USE CP;

CREATE TABLE IF NOT EXISTS error_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    notes TEXT, 
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS magicians (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT, 
    email TEXT, 
    location TEXT,
    index_letter_url TEXT,
    website TEXT,
    location_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS finished_locations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    location TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);