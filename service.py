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
    try: 
        cursor = database.cursor()
        row = cursor.execute('''SELECT name FROM sqlite_master 
                          WHERE name='messages';''').fetchone()
        database.commit()

        if row is not None:
            return True
    
    except sqlite3.Error as e:
        print("Exception in message_table_exists", e.args[0])
    
    return False

def create_message_table(database):
    """
    Creates the 'message' table in the database.
    Messages have a VARCHAR(150) text and an
    auto-increment INT id.

    database: A connection to a sqlite3 database.
    returns: Boolean
    """
    try:
        cursor = database.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                        text VARCHAR(150) NOT NULL);''')
        database.commit()
        return True
    
    except:
        print("Exception in create_message_table")
        return False

def insert_samples(database):
    """
    Inserts 10 sample messages into the database.
    Returns true if the messages were inserted, and
    false otherwise.

    database: A connection to a sqlite3 database.
    returns: Boolean
    """
    try:
        cursor = database.cursor()
        cursor.execute("INSERT INTO messages VALUES ('My favorite color is orange.');")
        database.commit()
        cursor.execute("INSERT INTO messages VALUES ('Welcome to my project!');")
        database.commit()
        cursor.execute("INSERT INTO messages VALUES ('How are you?');")
        database.commit()
        cursor.execute("INSERT INTO messages VALUES ('Three bears peer in the window.');")
        database.commit()
        cursor.execute("INSERT INTO messages VALUES ('Mayday, Mayday, Mayday');")
        database.commit()
        cursor.execute("INSERT INTO messages VALUES ('Where is the airport?');")
        database.commit()
        cursor.execute("INSERT INTO messages VALUES ('Have a nice weekend!');")
        database.commit()
        cursor.execute("INSERT INTO messages VALUES ('CRITICAL FIRE WARNING.');")
        database.commit()
        cursor.execute("INSERT INTO messages VALUES ('The ball is rolling up!');")
        database.commit()
        cursor.execute("INSERT INTO messages VALUES (?);", [("What is your dog's name?")])
        database.commit()
        return True

    except sqlite3.Error as e:
        print("Exception in insert_samples", e.args[0])
        return False

def get_count(database):
    """
    Gets the total count of messages in the database.
    Returns -1 if the operation failed.

    database: A connection to a sqlite3 database.
    returns: A number.
    """
    count = 0

    try:
        cursor = database.cursor()
        count = cursor.execute("SELECT COUNT(text) FROM messages;").fetchone()[0]
        database.commit()
    
    except sqlite3.Error as e:
        print("Exception in get_count.", e.args[0])
    
    return count

def get_message(database):
    """
    Gets a random message from the database.

    database: A connection to a sqlite3 database.
    returns: A text string or None.
    """
    message = None

    try:
        cursor = database.cursor()
        message = cursor.execute('''SELECT text FROM messages
                                    ORDER BY RANDOM()
                                    LIMIT 1;''').fetchone()
        database.commit()
        return message[0]

    except sqlite3.Error as e:
        print("Exception in get_message.", e.args[0])

    return message

def create_message(text, database):
    """
    Inserts a new message into the database. 
    Returns true if the message was created and
    false if there was an error.

    text: A string message.
    database: A connection to sqlite3 database.
    returns: Boolean
    """    
    try:
        cursor = database.cursor()
        cursor.execute("INSERT INTO messages VALUES (?);", [(text)])
        database.commit()
        return True

    except sqlite3.Error as e:
        print("Exception in create_message", e.args[0])
        return False

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

    while True:

        command = None
        with open('./coms.txt', 'r') as comsFile:
            command = comsFile.read()
        
        print("Command: ", command)

        if command == "GET":

            message = get_message(database)

            if message is not None:
                print("Message retrieved:", message)

                with open('./message.txt', 'w') as messageFile:
                    messageFile.write(message)
                
                with open('./coms.txt', 'w') as comsFile:
                    comsFile.write("OK")

        elif command == "POST":

            text = None
            with open('./message.txt', 'r') as messageFile:
                text = messageFile.read()

            if create_message(text, database):
                print("Message created:", text)

                with open('./coms.txt', 'w') as comsFile:  
                    comsFile.write("OK")
        
        time.sleep(5)
    
    return 0

if __name__ == '__main__':
    main()