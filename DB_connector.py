import mysql.connector
import logging
import argparse
from datetime import *
from Vars import *
from mysql.connector import errorcode

# TODO: Change file name to main

# Log files name
LOGGER_FILE = "logs.log"
# Logger format
FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
# Date format for queries
DATE_FORMAT = '%Y-%m-%d'



serving_24_massage = "24 hours serving: "
compare_daily_hourly_massage = "Compare daily to hourly reports: "


# TODO: think what to do about the fact i need Rev, IMPs from 2 queries maybe write a global ver (ask dror)

SERVING_24_EXPECTED_HOURS = 24
PERCENT_THRESHOLD = 0.01

DB_CONNECTION_CONFIG = {
  'user': 'omrig',
  'password': 'zUAv5hsG',
  'host': '10.0.32.223',
  'database': 'onetag',
  'raise_on_warnings': True
}
DB_CURSOR_CONFIG = {
    'buffered' : True,
    'dictionary' : True
}

# create logger
logging.basicConfig(format=FORMAT,level=logging.DEBUG,filename=LOGGER_FILE)

TODAY = date.today()


def generat_date(days_backwards):
    TODAY = date.today()
    generated_date = TODAY - timedelta(int(days_backwards))
    return datetime.strftime(generated_date, DATE_FORMAT)


def user_input():
    parser = argparse.ArgumentParser(description='Choose a test to run')
    parser.add_argument("-t","--test",dest="test",help='serving - 24 hours serving test'
                                        '\ncompare_daily_hourly - Compare daily hourly rev, IMPs test',
                        required=True)
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
    cursor = created_connection.cursor(**DB_CURSOR_CONFIG)
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
    postive_result = result * (-1)
    if threshold > postive_result:
        return True
    else:
        return False


# def round_mum(num, num_after_zero):
#     rounded_num = round(num, num_after_zero)
#     return rounded_num

# Creates connection to DB
cnx = create_connection(**DB_CONNECTION_CONFIG)


# Gets test to run from user via command line
args = user_input()

def serving_24_test():
    cursor = connect_to_DB(cnx)
    serving_24_cursor = execute_query(cursor=cursor, query=query_serving_24_hours.format(generat_date(1),TODAY))

    result_24_serving = fetch_result(cursor=serving_24_cursor)
    serving_hours = result_24_serving.get("hours_serving")

    # For testing purposes
    print serving_hours

    serving_24_cursor.close()

    if compare_results(SERVING_24_EXPECTED_HOURS,serving_hours):
        print serving_24_massage, True
    else:
        print serving_24_massage, False


def compare_daily_hourly_test():
    cursor_hourly = connect_to_DB(cnx)
    cursor_daily = connect_to_DB(cnx)

    hourly_cursor = execute_query(cursor=cursor_hourly, query=query_hourly_daily_match_hourly.format(generat_date(1), TODAY))
    daily_cursor = execute_query(cursor=cursor_daily, query=query_hourly_daily_match_daily.format(generat_date(1), TODAY))

    result_hourly = fetch_result(cursor=hourly_cursor)
    rev_hourly = round(result_hourly.get("Rev"),2)
    imps_hourly = round(result_hourly.get("IMPs"),2)

    result_daily = fetch_result(cursor=daily_cursor)
    rev_daily = round(result_daily.get("Rev"),2)
    imps_daily = round(result_daily.get("IMPs"),2)

    # For testing purposes
    print "rev hourly: ", rev_hourly
    print "imps hourly: ", imps_hourly

    print "rev daily: ", rev_daily
    print "imps daily: ", imps_daily

    percent_diff_rev = diff_in_percent(rev_hourly,rev_daily)
    percent_diff_imps = diff_in_percent(imps_hourly,imps_daily)

    hourly_cursor.close()
    daily_cursor.close()

    if compare_percent(PERCENT_THRESHOLD, percent_diff_rev) and compare_percent(percent_threshold, percent_diff_imps):
        print compare_daily_hourly_massage,True
    else:
        print compare_daily_hourly_massage,False

# TODO: option for 1 arg that will contain all test names to run in order to be able to run multiple tests.
def main():
    if args.test == "serving":
        serving_24_test()
    elif args.test == "compare_daily_hourly":
        compare_daily_hourly_test()
    elif args.test == "all":
        serving_24_test()
        compare_daily_hourly_test()


if __name__ == '__main__':
    main()
