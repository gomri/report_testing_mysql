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

key_daily_hourly = ['IMPs','Rev']

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
    parser.add_argument("serving",help='Run 24 hours serving test')
    parser.add_argument("daily_hourly",help="Run compare daily to hourly data test")
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


def fetch_result(cursor):
    result = cursor.fetchone()
    return result

def checking_results(expected, result):
    if expected == result:
        return True

def round_mum(num, num_after_zero):
    rounded_num = round(num, num_after_zero)
    return rounded_num

# Creates connection to DB
cnx = create_connection(**DB_connection_config)


# Gets test to run from user via command line
# test_to_run = user_input()

# if test_to_run.serving:
#     cursor = connect_to_DB(cnx)
#     serving_24_cursor = execute_query(cursor=cursor, query=query_serving_24_hours)
#
#     result_24_serving = fetch_result(cursor=serving_24_cursor,dict_keys=key_serving_24_hours)
#     print checking_results(expected=serving_24_expect_result, result=result_24_serving)
# TODO: Format test result so they are more indicative

# elif test_to_run.daily_hourly:
cursor_hourly = connect_to_DB(cnx)
cursor_daily = connect_to_DB(cnx)

hourly_cursor = execute_query(cursor=cursor_hourly, query=query_hourly_daily_match_hourly)
daily_cursor = execute_query(cursor=cursor_daily, query=query_hourly_daily_match_daily)

result_hourly = fetch_result(cursor=hourly_cursor)
Rev_hourly = round(result_hourly.get("Rev"),2)
IMPs_hourly = round(result_hourly.get("IMPs"),2)

result_daily = fetch_result(cursor=daily_cursor)
Rev_daily = round(result_daily.get("Rev"),2)
IMPs_daily = round(result_daily.get("IMPs"),2)

cursor_hourly.close()
cursor_daily.close()