-- Set database and user!
CREATE DATABASE IF NOT EXISTS retailer_db;
CREATE user IF NOT EXISTS 'retailer_user'@'localhost' identified BY 'retailer_pswd';
GRANT usage ON *.* TO 'retailer_user'@'localhost';
GRANT all privileges ON retailer_db.* TO 'retailer_user'@'localhost';
