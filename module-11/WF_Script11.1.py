#Rachel Shaw, Mark White, 
#Jason Shcriner,Rachel Theis
#CSD325



import mysql.connector
from mysql.connector import errorcode

import dotenv
from dotenv import dotenv_values


secrets = dotenv_values(".env")

# Connect to database
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database":secrets["DATABASE"],
    "raise_on_warnings": True
}
db = mysql.connector.connect(**config)
print(f"\n Databaseuser {config["user"]} connected to MYSQL on host {(config["host"])} with database {(config["database"])}")

#set Up cursor
cursor = db.cursor()

# Returns how many new clients in the past 6 months
def NewClients(cursor, title):

    cursor.execute("SELECT COUNT(*) AS client_count FROM clients WHERE registration_date BETWEEN '2023-02-20' AND '2023-08-20';")


    new_clients = cursor.fetchone()
    print("\n -- {} --".format(title))
    print(f"New Clients: {new_clients[0]}")

# returns average assets
def AverageAssets(cursor, title):
    cursor.execute("""SELECT AVG(assets_worth) AS average_assets_worth 
    FROM assets;""")
    
    average_assets = cursor.fetchall()
    print("\n -- {} --".format(title))

    for average_assets in average_assets:
        print("Average worth of assets: ${:,.2f}".format(average_assets[0]))

# returns how many clients have made over 10 transactions a month 
def high_transaction_months(cursor, title):
    cursor.execute("""
        SELECT clients_first_name AS fname, clients_last_name AS lname, 
               EXTRACT(MONTH FROM transaction_date) AS transaction_month, 
               COUNT(transaction_id) AS transaction_count
        FROM transactions 
        INNER JOIN accounts ON transactions.account_id = accounts.accounts_id 
        INNER JOIN clients ON accounts.clients_id = clients.clients_id
        GROUP BY clients.clients_id, transaction_month
        HAVING COUNT(transaction_id) > 10
        ORDER BY fname, transaction_month;
    """)
    
    high_transactions = cursor.fetchall()
    current_client = None
    
    print("\n -- {} --".format(title))
    
    for t in high_transactions:
        if current_client != (t[0], t[1]): #check for new client    
            if current_client is not None:
                print("\n")                #new line for new client
            current_client = (t[0], t[1])
            print(f"Client Name: {current_client[0]} {current_client[1]}")
        print(f" Month: 0{t[2]} 2023, Transactions: {t[3]}")  

def num_of_bills(cursor, title):
    cursor.execute("SELECT COUNT(*) AS bill_count FROM bills WHERE bills_date BETWEEN '2023-02-20' AND '2023-08-10'")
    

    bills = cursor.fetchone()
    print("\n -- {} --".format(title))
    print(f"Number of bills: {bills[0]}")


NewClients(cursor, "CLIENTS IN THE PAST 6 MONTHS")
AverageAssets(cursor, "AVERAGE CLIENT ASSETS")
high_transaction_months(cursor, "HIGH TRANSACTION CLIENTS (10+)")
num_of_bills(cursor, "BILLS IN THE PAST 6 MONTHS")

