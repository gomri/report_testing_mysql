import mysql.connector
import logging
from Vars import *
from mysql.connector import errorcode

# Log files name
LOGGER_FILE = "logs.log"
# Logger format
FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

DB_connection_config = {
  'user': 'omrig',
  'password': 'zUAv5hsG',
  'host': '10.0.32.223',
  'database': 'onetag',
  'raise_on_warnings': True
}


DB_cursor_config = {
    'buffered' : True,
    'dictionary' : True
}


# create logger
logging.basicConfig(format=FORMAT,level=logging.DEBUG,filename=LOGGER_FILE)


def create_connection(**args):
    try:
        cnx = mysql.connector.connect(**args)
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logging.critical("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logging.critical("Database does not exist")
        else:
            logging.critical(err)


def close_connection(cnx):
    cnx.close()


def connect_to_DB(created_connection):
    cursor = created_connection.cursor(**DB_cursor_config)
    return cursor


def execute_query(cursor,query):
    cursor.execute(query)
    return cursor


cnx = create_connection(**DB_connection_config)


cursor = connect_to_DB(cnx)
execute_query(cursor=cursor, query=testing)


# for row in cursor:
#     print "{entity_name}, {date_interval}".format(**row)