import mysql.connector
from mysql.connector import errorcode
import dotenv
from dotenv import dotenv_values

secrets = dotenv_values('.env')
config = {
    'user': secrets['USER'],
    'password': secrets["PASSWORD"],
    'host': secrets['HOST'],     
    'database': secrets['DATABASE'], 
    'raise_on_warnings': True
}

try:
    db = mysql.connector.connect(**config)

    print("\n Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"], config["database"]))

    cursor = db.cursor()

    query_one = '''
    SELECT studio_id, studio_name FROM studio;'''

    cursor.execute(query_one)

    results_one = cursor.fetchall()
    for row in results_one:
        print(f"studio_id: {row[0]}, studio_name: {row[1]}")
    
    query_two = '''
    SELECT genre_id, genre_name FROM genre;'''

    cursor.execute(query_two)

    print(" ")

    results_two = cursor.fetchall()
    for row in results_two:
        print(f"genre_id: {row[0]}, genre_name: {row[1]}")
    
    
    print(" ")
    
    query_three = """SELECT film_name, film_runtime
    FROM film WHERE film_runtime < 120;"""

    cursor.execute(query_three)

    results_three = cursor.fetchall()
    for row in results_three:
        print(f"Film: {row[0]}, Runtime: {row[1]} minutes")
    
    print(" ")
    
    query_four = '''
    SELECT film_name, film_director FROM film ORDER BY film_director, film_name;'''

    cursor.execute(query_four)

    print(" ")

    results_four = cursor.fetchall()
    for row in results_four:
        print(f"film_name: {row[0]}, film_director: {row[1]}")
    
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print(" The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print(" The specified database does not exist")

    else:
        print(err)
finally:
    db.close()