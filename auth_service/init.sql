-- Run the following if MySQL version is buggy, to force the whole execution, script should do all the things fine.
-- mysql --force -uroot -p < init.sql

-- User for the database
DROP USER 'auth_user'@'%';
CREATE USER 'auth_user'@'%' IDENTIFIED BY 'Auth123';

CREATE DATABASE auth;

GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'%';

-- Database directives from here on
USE auth;

CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT INTO user (email, password) VALUES ('jbruno.coding@gmail.com', 'secret');