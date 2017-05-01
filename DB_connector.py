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

serving_24_massage = "24 hours serving: "
compare_daily_hourly_massage = "Compare daily to hourly reports: "


# TODO: think what to do about the fact i need Rev, IMPs from 2 queries maybe write a global ver (ask dror)

percent_threshold = 0.01  # TODO: ask michal what she wants the threshold to be

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
    parser.add_argument("test_num",type=int,help='1. 24 hours serving'
                                                        '\n2. Compare daily hourly rev, IMPs')
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


def diff_in_percent(num1,num2):
    percent_diff = 100 * (num2-num1) / num1
    return percent_diff


def compare_results(expected, result):
    if expected == result:
            return True
    else:
        return False


def compare_percent(threshold, result):
    if threshold > result:
        return True
    else:
        return False


# def round_mum(num, num_after_zero):
#     rounded_num = round(num, num_after_zero)
#     return rounded_num

# Creates connection to DB
cnx = create_connection(**DB_connection_config)


# Gets test to run from user via command line
test_to_run = user_input()

if test_to_run.test_num == 1:
    cursor = connect_to_DB(cnx)
    serving_24_cursor = execute_query(cursor=cursor, query=query_serving_24_hours)

    result_24_serving = fetch_result(cursor=serving_24_cursor)
    serving_hours = result_24_serving.get("hours_serving")

    serving_24_cursor.close()

    if compare_results(serving_24_expect_result,serving_hours):
        print serving_24_massage, True
    else:
        print serving_24_massage, False

elif test_to_run.test_num  == 2:
    cursor_hourly = connect_to_DB(cnx)
    cursor_daily = connect_to_DB(cnx)

    hourly_cursor = execute_query(cursor=cursor_hourly, query=query_hourly_daily_match_hourly)
    daily_cursor = execute_query(cursor=cursor_daily, query=query_hourly_daily_match_daily)

    result_hourly = fetch_result(cursor=hourly_cursor)
    rev_hourly = round(result_hourly.get("Rev"),2)
    imps_hourly = round(result_hourly.get("IMPs"),2)

    result_daily = fetch_result(cursor=daily_cursor)
    rev_daily = round(result_daily.get("Rev"),2)
    imps_daily = round(result_daily.get("IMPs"),2)

    percent_diff_rev = diff_in_percent(rev_hourly,rev_daily)
    percent_diff_imps = diff_in_percent(imps_hourly,imps_daily)

    hourly_cursor.close()
    daily_cursor.close()

    if compare_percent(percent_threshold, percent_diff_rev) and compare_percent(percent_threshold, percent_diff_imps):
        print compare_daily_hourly_massage,True
    else:
        print compare_daily_hourly_massage,False


