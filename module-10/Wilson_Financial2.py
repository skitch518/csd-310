import mysql.connector
from mysql.connector import errorcode
import dotenv
from dotenv import dotenv_values


#File modified from:
#Title: db_init_2022.sql
#Author: Professor Sampson
#Date: 1 Aug 2022
#Description: movies database initialization script.


# Load database connection credentials from .env file
secrets = dotenv_values('.env')
config = {
    'user': secrets['USER'],
    'password': secrets["PASSWORD"],
    'host': secrets['HOST'],
    'database': secrets['DATABASE'],     
    'raise_on_warnings': True
}

try:
    # Connect to MySQL database
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    cursor.execute("USE `wilson_financial`;")
    print("\nDatabase user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"], config["database"]))
    
    
    # Create the clients table
    cursor.execute("""CREATE TABLE clients (
        clients_id INT NOT NULL AUTO_INCREMENT,
        clients_first_name VARCHAR(75) NOT NULL,
        clients_last_name VARCHAR(75) NOT NULL,
        clients_phone VARCHAR(75) NOT NULL,
        clients_email VARCHAR(75) NOT NULL,
        registration_date DATE NOT NULL,
        PRIMARY KEY (clients_id)
    );""")

    # Create the accounts table
    cursor.execute("""CREATE TABLE accounts (
        accounts_id INT NOT NULL AUTO_INCREMENT,
        accounts_type VARCHAR(75) NOT NULL,
        clients_id INT NOT NULL,
        PRIMARY KEY (accounts_id),
        FOREIGN KEY (clients_id) REFERENCES clients(clients_id)
    );""")

    # Create the services table
    cursor.execute("""CREATE TABLE services (
        services_id INT NOT NULL AUTO_INCREMENT,
        services_type VARCHAR(75) NOT NULL,
        services_price INT NOT NULL,
        PRIMARY KEY (services_id)
    );""")

    # Create the bills table and set foreign key constraints
    cursor.execute("""CREATE TABLE bills (
        bills_id INT NOT NULL AUTO_INCREMENT,
        bills_amount INT NOT NULL,
        bills_date DATE NOT NULL,
        services_id INT NOT NULL,
        clients_id INT NOT NULL,
        PRIMARY KEY (bills_id),
        FOREIGN KEY (clients_id) REFERENCES clients(clients_id),
        FOREIGN KEY (services_id) REFERENCES services(services_id)
    );""")

   
    # Create the assets table
    cursor.execute("""CREATE TABLE assets (
        assets_id INT NOT NULL AUTO_INCREMENT,
        assets_type VARCHAR(75) NOT NULL,
        assets_worth INT NOT NULL,
        assets_desc VARCHAR(255) NOT NULL,
        clients_id INT NOT NULL,
        PRIMARY KEY (assets_id),
        FOREIGN KEY (clients_id) REFERENCES clients(clients_id)
    );""")

    # Create the transactions table
    cursor.execute("""CREATE TABLE transactions (
        transaction_id INT NOT NULL AUTO_INCREMENT,
        transaction_type VARCHAR(75) NOT NULL,
        transaction_amount INT NOT NULL,
        transaction_date DATE NOT NULL,
        account_id INT NOT NULL,
        PRIMARY KEY (transaction_id),
        FOREIGN KEY (account_id) REFERENCES accounts(accounts_id)
    );""")

    # Insert sample client records
    cursor.execute("""INSERT INTO clients (clients_first_name, clients_last_name, clients_phone, clients_email, registration_date)
    VALUES
    ('Olivia', 'Anderson', '555-2783', 'oliviaanderson23@gmail.com', '2023-05-12'),
    ('Liam', 'Carter', '555-9147', 'liamcarter39@gmail.com', '2022-03-18'),
    ('Ethan', 'Thompson', '937-5555', 'ethanthompson@gmail.com', '2021-07-12'),
    ('Sarah', 'Evans', '843-5555', 'sarahevans42@gmail.com', '2024-02-14'),
    ('Brandon', 'Washington', '555-2604', 'brandonwashington555@gmail.com', '2021-04-30'),
    ('Tina', 'Scott', '555-6502', 'tinascott42@gmail.com', '2023-02-02');""")

    # Insert sample accounts records
    cursor.execute("""INSERT INTO accounts (accounts_type, clients_id)
    VALUES
    ('Savings', 1),
    ('Checking', 2),
    ('Business', 3),
    ('Savings', 4),
    ('Checking', 5),
    ('Business', 6);""")

    # Insert sample services records
    cursor.execute("""INSERT INTO services (services_type, services_price)
    VALUES
    ('Consultation', 150),
    ('Financial Planning', 300),
    ('Investment Advisory', 250),
    ('Insurance', 180),
    ('Tax Preparation', 200),
    ('Loan Services', 500);""")

    # Insert sample assets records
    cursor.execute("""INSERT INTO assets (assets_type, assets_worth, assets_desc, clients_id)
    VALUES
    ('House', 500000, '4-bedroom house in suburb', 1),
    ('Car', 25000, '2018 Honda Accord', 2),
    ('Business', 1000000, 'Small manufacturing business', 3),
    ('Real Estate', 800000, 'Commercial building', 4),
    ('Stocks', 150000, 'Portfolio of stocks', 5),
    ('Land', 200000, '5 acres of agricultural land', 6);""")

    # Insert sample bills records
    cursor.execute("""INSERT INTO bills (bills_amount, bills_date, services_id, clients_id)
    VALUES
    (150, '2023-06-01', 1, 1),
    (300, '2023-07-15', 2, 2),
    (250, '2023-08-10', 3, 3),
    (180, '2024-01-05', 4, 4),
    (200, '2023-12-20', 5, 5),
    (500, '2023-11-30', 6, 6);""")

    # Insert sample transactions records
    cursor.execute("""INSERT INTO transactions (transaction_type, transaction_amount, transaction_date, account_id)
    VALUES
    ('Deposit', 2000, '2023-06-01', 1),
    ('Withdrawal', 500, '2023-07-10', 2),
    ('Transfer', 1000, '2023-08-01', 3),
    ('Deposit', 1200, '2024-01-10', 4),
    ('Withdrawal', 300, '2023-12-15', 5),
    ('Deposit', 1500, '2023-11-25', 6);""")

    # Commit the changes
    db.commit()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist.")
    else:
        print(err)

finally:
    if db.is_connected():
        db.close()