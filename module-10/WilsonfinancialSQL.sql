-- Rachel Shaw, Rachel Theis, Jason Schriner, Mark White
-- Wilson Financial Database Set up Script



-- define which database we're using
USE Wilson_Financial;

-- drop database user if exists 
DROP USER IF EXISTS 'WFUser'@'localhost';

-- create database user 
CREATE USER 'WFUser'@'localhost' IDENTIFIED WITH mysql_native_password BY [password];

-- grant all privileges to the database to user WFUSER on localhost 
GRANT ALL PRIVILEGES ON Wilson_Financial.* TO 'WFUser'@'localhost';


-- drop tables if they are present
DROP TABLE IF EXISTS clients;
DROP TABLE IF EXISTS bills;
DROP TABLE IF EXISTS transactions
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS services;
DROP TABLE IF EXISTS assets;




-- create the clients table 
CREATE TABLE clients (
    clients_id     INT             NOT NULL        AUTO_INCREMENT,
    clients_first_name   VARCHAR(75)     NOT NULL,
    clients_last_name VARCHAR(75) NOT NULL,
    clients_phone VARCHAR(75) NOT NULL,
    clients_email VARCHAR(75) NOT NULL,
    registration_date DATE NOT NULL,
    PRIMARY KEY (clients_id)
); 

-- create the accounts table 
CREATE TABLE accounts (
accounts_id INT NOT NULL AUTO_INCREMENT,
accounts_type VARCHAR(75) NOT NULL,
clients_id INT NOT NULL,
PRIMARY KEY (accounts_id),
FOREIGN KEY (clients_id) REFERENCES clients(clients_id)
); 

-- Create services table
CREATE TABLE services (
    services_id INT NOT NULL AUTO_INCREMENT,
    services_type VARCHAR(75) NOT NULL,
    services_price INT NOT NULL,
    PRIMARY KEY (services_id)
);

-- create bills table
CREATE TABLE bills (
    bills_id INT NOT NULL AUTO_INCREMENT,
    bills_amount INT NOT NULL,
    bills_date DATE NOT NULL,
    services_id INT NOT NULL,
    clients_id INT NOT NULL,
    PRIMARY KEY (bills_id),
    FOREIGN KEY (clients_id) REFERENCES clients(clients_id),
    FOREIGN KEY (services_id) REFERENCES services(services_id)
);

--create assets table
CREATE TABLE assets (
    assets_id INT NOT NULL AUTO_INCREMENT,
    assets_type VARCHAR(75) NOT NULL,
    assets_worth INT NOT NULL,
    assets_desc VARCHAR(255) NOT NULL,
    clients_id INT NOT NULL,
    PRIMARY KEY (assets_id),
    FOREIGN KEY (clients_id) REFERENCES clients(clients_id)
    );

-- create transactions table
CREATE TABLE transactions (
        transaction_id INT NOT NULL AUTO_INCREMENT,
        transaction_type VARCHAR(75) NOT NULL,
        transaction_amount INT NOT NULL,
        transaction_date DATE NOT NULL,
        account_id INT NOT NULL,
        PRIMARY KEY (transaction_id),
        FOREIGN KEY (account_id) REFERENCES accounts(accounts_id)
    );

-- insert values into clients
INSERT INTO clients (clients_first_name, clients_last_name, clients_phone, clients_email, registration_date) VALUES
    ('Olivia', 'Anderson', '555-2783', 'oliviaanderson23@gmail.com', '2023-05-12'),
    ('Liam', 'Carter', '555-9147', 'liamcarter39@gmail.com', '2022-03-18'),
    ('Ethan', 'Thompson', '937-5555', 'ethanthompson@gmail.com', '2021-07-12'),
    ('Sarah', 'Evans', '843-5555', 'sarahevans42@gmail.com', '2024-02-14'),
    ('Brandon', 'Washington', '555-2604', 'brandonwashington555@gmail.com', '2021-04-30'),
    ('Tina', 'Scott', '555-6502', 'tinascott42@gmail.com', '2023-02-02');

-- insert values into accounts
INSERT INTO accounts (accounts_type, clients_id)
    VALUES
    ('Savings', 1),
    ('Checking', 2),
    ('Business', 3),
    ('Savings', 4),
    ('Checking', 5),
    ('Business', 6);

-- insert values into services
INSERT INTO services (services_type, services_price)
    VALUES
    ('Consultation', 150),
    ('Financial Planning', 300),
    ('Investment Advisory', 250),
    ('Insurance', 180),
    ('Tax Preparation', 200),
    ('Loan Services', 500);

-- insert values into assets
INSERT INTO assets (assets_type, assets_worth, assets_desc, clients_id)
    VALUES
    ('House', 500000, '4-bedroom house in suburb', 1),
    ('Car', 25000, '2018 Honda Accord', 2),
    ('Business', 1000000, 'Small manufacturing business', 3),
    ('Real Estate', 800000, 'Commercial building', 4),
    ('Stocks', 150000, 'Portfolio of stocks', 5),
    ('Land', 200000, '5 acres of agricultural land', 6);

--insert values into bills
INSERT INTO bills (bills_amount, bills_date, services_id, clients_id)
    VALUES
    (150, '2023-06-01', 1, 1),
    (300, '2023-07-15', 2, 2),
    (250, '2023-08-10', 3, 3),
    (180, '2024-01-05', 4, 4),
    (200, '2023-12-20', 5, 5),
    (500, '2023-11-30', 6, 6);

--insert values into transactions
INSERT INTO transactions (transaction_type, transaction_amount, transaction_date, account_id)
    VALUES
    ('Deposit', 2000, '2023-06-01', 1),
    ('Withdrawal', 500, '2023-07-10', 2),
    ('Transfer', 1000, '2023-08-01', 3),
    ('Deposit', 1200, '2024-01-10', 4),
    ('Withdrawal', 300, '2023-12-15', 5),
    ('Deposit', 1500, '2023-11-25', 6);