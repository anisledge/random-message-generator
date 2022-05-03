# Random Message Generator Microservice
# Anastasia Sledgianowski
# 5/2/2022
# CS361

import sqlite3
import time

DATABASE_PATH = "./message.db"

def connect_to_database(path):
    """
    path: A string path to the database file. 
    returns: A connection to a sqlite3 database or None.
    """
    connection = None

    try: 
        connection = sqlite3.connect(path)

    except sqlite3.Error as e:
        print("An error occurred while connecting to the database: ", e.args[0])

    return connection

def message_table_exists(database):
    """
    Returns true if there is a 'message' table in the 
    database, and false otherwise.

    database: A connection to a sqlite3 database.
    returns: Boolean
    """
    pass

def create_message_table(database):
    """
    Creates the 'message' table in the database.
    Messages have a VARCHAR(150) text and an
    auto-increment INT id.

    database: A connection to a sqlite3 database.
    returns: Boolean
    """
    pass

def insert_samples(database):
    """
    Inserts 10 sample messages into the database.
    Returns true if the messages were inserted, and
    false otherwise.

    database: A connection to a sqlite3 database.
    returns: Boolean
    """
    pass

def get_count(database):
    """
    Gets the total count of messages in the database.
    Returns -1 if the operation failed.

    database: A connection to a sqlite3 database.
    returns: A number.
    """
    count = 0

    try:
        cursor = con.cursor()
        count = cursor.execute('''SELECT COUNT(text) FROM messages;''').fetchone()[0]
        con.commit()
        return count
    
    except:
        print("Exception in get_count.")
        return -1

def get_message(database):
    """
    Gets a random message from the database.

    database: A connection to a sqlite3 database.
    returns: A text string or None.
    """
    message = None

    try:
        cursor = con.cursor()
        message = cursor.execute('''SELECT text FROM messages
                                    ORDER BY RANDOM()
                                    LIMIT 1;''')[0]
        con.commit()
        return message

    except:
        print("Exception in get_message.")

    return message

def create_message(message, database):
    """
    Inserts a new message into the database. 
    Returns true if the message was created and
    false if there was an error.

    message: A string message.
    database: A connection to sqlite3 database.
    returns: Boolean
    """    
    pass

def main():
    """
    Creates a database connection and initializes the database if necessary.
    Scans the coms file for GET and POST requests.
    Responds to GET and POST requests.
    """

    database = connect_to_database(DATABASE_PATH)

    if database is None:
        print("Exiting microservice: Cannot connect to database.")
        return 1

    if not message_table_exists(database):
        print("Message table does not exist. Creating message table.")
        create_message_table(database)

    count = get_count(database)
    if count <= 0:
        print("There are no messages in the database. Adding sample messages.")
        insert_samples(database)
    
    print("*****************************************************")
    print("The Random Message Generator Microservice is running.")
    print("Enter 'Ctrl-C' to exit.")

    with open('./coms.txt', 'w+') as comsFile:
        
        with open('./message.txt') as messageFile: 

            while True:
                command = comsFile.readline()

                if command == "GET":
                    message = get_message(database)

                    if message is not None:
                        comsFile.write("OK")

                else if command == "POST":
                    text = messageFile.readline()

                    if create_message(text, database):
                        comsFile.write("OK")
                
                time.sleep(5)

if __name__ == '__main__':
    main()