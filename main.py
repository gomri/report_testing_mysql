import DB_connector
from Vars import *
from datetime import date, timedelta
import logging
import mysql.connector
from mysql.connector import errorcode

# Creates the logger and sets it's logs format
FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='logs.log', level=logging.DEBUG, format=FORMAT)


def connect_to_db():
    try:
        cnx = mysql.connector.connect(user='omrig',
                                      password='zUAv5hsG',
                                      host='10.0.32.223',  # Slave
                                      # Master '10.0.32.33',
                                      database='onetag')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logging.critical('Something is wrong with your user name or password')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logging.critical('Database does not exist')
        else:
            logging.critical(err)
    else:
        logging.info('connection successful')
        print 'connection successful'


def create_connections():
    try:
        cursor = DB_connector.cnx.cursor(buffered=True)
        return cursor
    except Exception as e:
        logging.critical(e)


def serving_24_hours(cursor, query):
    try:
        start_date = generat_date(2)
        end_date = generat_date(1)

        cursor.execute(query.format(start_date, end_date))
        return cursor
    except Exception as e:
        logging.critical(e)
        raise e


def imps_rev_last_5_days(cursor, query, entity_id_list):

    try:
        start_date = today
        end_date = generat_date(5)
        # print query.format(start_date, end_date, entity_id_list)

        cursor.execute(query.format
            (
            end_date,
            start_date,
            entity_ids
        )
        )
        return cursor
    except Exception as e:
        logging.critical(e)
        raise e


def fetch_data(cursor):
    row = cursor.fetchall()
    if row is None or row == []:
        logging.critical('No data was returned by query')
    elif row is not None:
        while row is not None:
            query_response = list(row)
            row = cursor.fetchone()
        return query_response


def close_connections(cursor):
    cursor.close()
    DB_connector.cnx.close()


def check_24_hours_serving(alist):
    if len(alist) == 24:
        test_result = True
        return test_result
    elif len(alist) != 24:
        test_result = False
        return test_result


# sorts the data from the imps, rev last 5 days query into lists containing one entity id and all it's dates
def sort_data(lst, id_of_entity):
    sorted_data = []
    for element in lst:
        if element[0] == id_of_entity:
            sorted_data.append(element)
    return sorted(sorted_data)


def check_delta_last_5_days(num, delta_percent):
    if num < delta_percent:
        return True
    elif num >= delta_percent:
        return False


# Generats todays date
today = date.today()


# Generats any date depending on what the amount of days backwards yuu pick using the timedelta(days backwards) function
def generat_date(days_backwards):
    generated_date = today - timedelta(int(days_backwards))
    return generated_date


def test_result_formater(test_name, result):
    formatted_result = str(test_name) + str(result)
    return formatted_result


# serving_24_hours_test_result = check_24_hours_serving(result_24_hour_serving)

# print test_result_formater("\n24 Hours exist: ", serving_24_hours_test_result)


cursor = create_connections()

imps_rev_last_5_days(cursor, query_imps_rev_last_days_5, entity_ids)

result_imps_rev_last_5_days = fetch_data(cursor)

print len(sort_data(result_imps_rev_last_5_days,11))

for entity_id in entity_ids:
    if len(sort_data(result_imps_rev_last_5_days, entity_id)) > 5:
        # print "s"
        continue
    for i in range(2):
        if i == 0:
            # print "y"
            lst2 = [item[2] for item in sort_data(result_imps_rev_last_5_days, entity_id)]
            print lst2
            avrg_4_days_imps = (sum(lst2[:-1]) / len(lst2[:-1])) / len(lst2)
            yesterdays_imps = lst2[-1]
            imps_last_5_days_delta = round(((avrg_4_days_imps / yesterdays_imps) / yesterdays_imps) * 100, 2)
        elif i == 1:
            # print "x"
            lst3 = [item[3] for item in sort_data(result_imps_rev_last_5_days, entity_id)]
            avrg_4_days_rev = (sum(lst3[:-1]) / len(lst3[:-1])) / len(lst3)
            yesterdays_rev = lst3[-1]
            rev_last_5_days_delta = round(((avrg_4_days_rev / yesterdays_rev) / yesterdays_rev) * 100, 2)


result_test_delta_rev = check_delta_last_5_days(rev_last_5_days_delta, min_delta)
result_test_delta_imps = check_delta_last_5_days(imps_last_5_days_delta, min_delta)


if result_test_delta_rev and result_test_delta_imps:
    print test_result_formater("\nIMPs and Rev last 4 days delta: ", True)


print result_test_delta_imps
print result_test_delta_rev


close_connections(cursor)


# cursor = serving_24_hours(cursor, query_serving_24_hours)
#
#  result_24_hour_serving = fetch_data(cursor)
