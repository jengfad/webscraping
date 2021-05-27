USE CP;

CREATE TABLE IF NOT EXISTS ct.error_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    notes TEXT, 
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ct.countertop (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email TEXT, 
    location TEXT,
    phone TEXT,
    website TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);