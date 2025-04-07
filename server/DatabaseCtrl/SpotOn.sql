DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Destinations;
DROP TABLE IF EXISTS Carparks;

-- Create Carparks table first to avoid Foreign Key issues
CREATE TABLE
IF NOT EXISTS Carparks
(
    carpark_id VARCHAR
(50) PRIMARY KEY,
    address VARCHAR
(100) NOT NULL, 
    X_coord DECIMAL
(9,4) NOT NULL,
    Y_coord DECIMAL
(9,4) NOT NULL,
    carpark_type VARCHAR
(100),
    parking_system VARCHAR
(100),
    short_term_parking VARCHAR
(100),
    free_parking VARCHAR
(100),
    night_parking BOOLEAN, 
    carpark_decks INT,
    gantry_height DECIMAL
(3,2),
    carpark_basement BOOLEAN
);

-- Create Users table
CREATE TABLE
IF NOT EXISTS Users
(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR
(50) NOT NULL UNIQUE,
    email VARCHAR
(100) NOT NULL UNIQUE,
    password VARCHAR
(100) NOT NULL
);

-- Create Destinations table
CREATE TABLE
IF NOT EXISTS Destinations
(
    destination_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    carpark_id VARCHAR
(50) NOT NULL,
    datetime VARCHAR
(50) NOT NULL,
    FOREIGN KEY
(user_id) REFERENCES Users
(user_id) ON
DELETE CASCADE,
    FOREIGN KEY (carpark_id)
REFERENCES Carparks
(carpark_id) ON
DELETE CASCADE
);
