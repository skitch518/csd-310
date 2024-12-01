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

def show_films(cursor, title):
        #method to execute an inner join on all tables,
        #iterate over the dataset and output the results to the terminal window

        #inner join query
        cursor.execute("""SELECT film_name AS Name, film_director AS Director, 
                        genre_name AS Genre,studio_name AS 'Studio Name'
                        FROM film 
                        INNER JOIN genre ON film.genre_id = genre.genre_id 
                        INNER JOIN studio ON film.studio_id = studio.studio_id""")

        #get the results from the cursor object
        films =cursor.fetchall()

        print("\n -- {} --".format(title))

        #iterate over the film data set and display the results
        for film in films:
            print("Film Name: {}\nDirector: {}\nGenre Name ID: {} \nStudio Name: {}\n".format(film[0], film[1], film [2], film[3]))

def insert_genre_and_film(cursor):
    # Insert a new genre into the genre table
    cursor.execute("""INSERT INTO genre(genre_name)
                   VALUES('Action/Thriller')""")

    # Insert a new film into the film table
    cursor.execute("""INSERT INTO film(film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id) 
                   VALUES('Man on Fire', '2004', '146', 'Tony Scott',
                   (SELECT studio_id FROM studio WHERE studio_name = '20th Century Fox'),
                   (SELECT genre_id FROM genre WHERE genre_name = 'Action/Thriller'))""")

def change_genre(cursor):
    cursor.execute("""UPDATE genre
                   SET genre_name = 'Horror'
                   WHERE genre_id = (SELECT genre_id
                   FROM film
                   WHERE film_name = 'Alien')""")

def delete_record(cursor):
    cursor.execute("""DELETE FROM film
        WHERE film_name = 'Gladiator'
        AND film_releaseDate = '2000'
        AND film_runtime = '155'
        AND film_director = 'Ridley Scott'
        AND studio_id = (SELECT studio_id FROM studio WHERE studio_name = 'Universal Pictures')
        AND genre_id = (SELECT genre_id FROM genre WHERE genre_name = 'Drama')
    """)



try:
    db = mysql.connector.connect(**config)

    print("\n Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"], config["database"]))

    cursor = db.cursor()

    title = "Displaying Films"
    #display current database
    show_films(cursor, title)

    title = "Displaying Films After Insert"

    #execute the insert
    insert_genre_and_film(cursor)
    
    #display updated database
    show_films(cursor, title)

    title = "Displaying Films After Update - Changed Alien to Horror"

    #change genre
    change_genre(cursor)
    
    #display updated database
    show_films(cursor, title)

    title = "Displaying Films After Delete"
    #delete record
    delete_record(cursor)

    #display updated database
    show_films(cursor, title)

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print(" The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print(" The specified database does not exist")

    else:
        print(err)
finally:
    db.close()