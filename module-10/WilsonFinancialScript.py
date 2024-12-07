# Case Studies Milestone 2 Python Script
# Rachel Shaw, Jason Schriner, Mark White, Rachel Theis

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

def show_clients(cursor, title):
    cursor.execute("SELECT clients_first_name AS 'First Name', clients_last_name AS 'Last Name', clients_phone AS 'Phone', clients_email AS 'Email', registration_date AS 'registration date' FROM clients")
    client = cursor.fetchall()
    print("\n -- {} --".format(title))

    for client in client:
        print("Client Name: {} {}\nPhone Number: {}\nEmail: {}\nRegistration Date: {}\n".format(client[0], client[1], client[2], client[3], client[4]))

def show_accounts(cursor, title):
    cursor.execute("SELECT clients_first_name AS fname, clients_last_name AS lname, accounts_type AS Type from accounts INNER JOIN clients ON accounts.clients_id = clients.clients_id")
    account = cursor.fetchall()
    print("\n -- {} --".format(title))
    for account in account:
        print("Client Name: {} {}\n Account Type: {}\n".format(account[0], account[1], account[2]))

def show_services (cursor, title):
    cursor.execute("SELECT services_type AS type, services_price AS price FROM services")
    service = cursor.fetchall()
    print("\n -- {} --".format(title))
    for service in service:
        print("Service: {}\n Price: {}\n".format(service[0], service[1]))

def show_bills(cursor, title):
    cursor.execute("SELECT clients_first_name AS fname, clients_last_name AS lname,  services_type AS service, bills_amount AS amount, bills_date AS date FROM bills INNER JOIN clients ON bills.clients_ID = clients.clients_ID INNER JOIN services ON bills.services_id = services.services_id")
    bill = cursor.fetchall()
    print("\n -- {} --".format(title))
    for bill in bill:
        print("Client Name: {}{}\n Service: {}\n Billed Amount: {}\n Billing Date: {}\n".format(bill[0], bill[1],bill[2],bill[3], bill[4]))

def show_assets(cursor, title):
    cursor.execute("SELECT clients_first_name AS fname, clients_last_name AS lname, assets_desc AS 'assetname', assets_type AS type, assets_worth AS worth FROM assets INNER JOIN clients ON assets.clients_id = clients.clients_id")
    asset = cursor.fetchall()
    print("\n -- {} --".format(title))
    for asset in asset:
        print("Client Name: {} {}\n Asset: {} Type: {} Worth: ${}".format(asset[0],asset[1],asset[2],asset[3], asset[4]))

def show_transactions(cursor, title):
    cursor.execute("SELECT clients_first_name AS fname,  clients_last_name AS lname, accounts_type AS account, transaction_type AS Type, transaction_amount AS amount, transaction_date AS date FROM transactions INNER JOIN accounts ON transactions.account_id = accounts.accounts_id INNER JOIN clients ON accounts.clients_id = clients.clients_id")
    transaction = cursor.fetchall()
    print("\n -- {} --".format(title))

    # Displays "-" and "+" depending on transaction type
    for transaction in transaction:
        if transaction[3] == 'Withdrawal':
            amount = "-${}".format((transaction[4]))
        elif transaction [3] == 'Transfer':
            amount = "-${}".format((transaction[4]))
        else:
            amount = "+${}".format((transaction[4]))
        
        print("Client Name: {} {}\n Account: {}\n Transaction: {}\n Amount: {}\n Date: {}\n".format(transaction[0], transaction[1], transaction[2], transaction[3], amount, transaction[5]))
    

show_services(cursor, "SERVICES")
show_clients(cursor, "CLIENTS")
show_accounts(cursor, "ACCOUNTS")
show_bills(cursor, "BILLING RECORDS")
show_transactions(cursor, "TRANSACTION RECORDS")
