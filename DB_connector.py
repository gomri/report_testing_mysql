import mysql.connector
import logging
import argparse
from Vars import *
from mysql.connector import errorcode

# Log files name
LOGGER_FILE = "logs.log"
# Logger format
FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

serving_24_expect_result = 24

key_serving_24_hours = "hours_serving"

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


def user_input():
    parser = argparse.ArgumentParser(description='Choose a test to run')
    parser.add_argument("serving",help='run 24 hours serving test')
    return parser.parse_args()


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


def execute_query(cursor, query):
    cursor.execute(query)
    return cursor


def fetch_result(cursor, dict_keys):
    serving_hours = cursor.fetchone().get(dict_keys)
    return serving_hours


def checking_results(expected, result):
    if expected == result:
        return True

# Creates connection to DB
cnx = create_connection(**DB_connection_config)
cursor = connect_to_DB(cnx)

# Gets test to run from user via command line
test_to_run = user_input()

if test_to_run.serving:

    serving_24_cursor = execute_query(cursor=cursor, query=query_serving_24_hours)
    result_24_serving = fetch_result(cursor=serving_24_cursor,dict_keys=key_serving_24_hours)
    print checking_results(expected=serving_24_expect_result, result=result_24_serving)