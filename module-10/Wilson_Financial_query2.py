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

    #Query to find how many new clients in the last 6 months
    cursor.execute("""SELECT COUNT(*) AS client_count FROM clients
    WHERE registration_date >= CURDATE() - INTERVAL 6 MONTH;""")

    #Get the results
    new_clients = cursor.fetchone()
    
    #Print the number of new clients
    print(f"Number of clients registered in the last 6 months: {result[0]}")

    #Query to find the average assets
    cursor.execute("""SELECT AVG(assets_worth) AS average_assets_worth
    #FROM assets;""")
    
    #Retrieve the results
    average_balance = cursor.fetchone

    #Print the average assets
    print(f"The average assets worth is: {average_balance}")
    
    #Query to find out which clients had more than 10 transactions in the last month
    cursor.execute("""SELECT account_id, clients_first_name, clients_last_name, COUNT(transaction_id) AS transaction_count
    FROM clients
    JOIN transactions ON account_id = account_id
    WHERE transaction_date >= CURDATE() - INTERVAL 1 MONTH
    GROUP BY account_id, clients_first_name, clients_last_name
    HAVING COUNT(transaction_id) > 10;""")

    #Retrieve the results
    repeat_customer = cursor.fetchall

    #Print the customers who had more than 10 transactions
    print(repeat_customer)

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
