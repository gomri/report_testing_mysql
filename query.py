import DB_connector
from Vars import *
from utilities import *
from Appliaction_logging import *


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


def imps_rev_last_5_days(cursor, query, entity_name):
    try:
        start_date = today
        end_date = generat_date(5)

        # print query.format(start_date, end_date, entity_name)
        """
        
        """
        cursor.execute(query.format
            (
            end_date,
            start_date,
            entity_name
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


# def convert_to_dict(data,entity_name):
#     result_dict = {}
#     for i in range(len(data)):
#         for ii in range(len(data[i])):
#             if data[i][0] == entity_name:
#                 temp_dict = {
#                     data[i][0]:{
#                         data[i][1]: {
#                             "IMPs": data[i][2],
#                             "Rev": data[i][3]
#                         }
#                     }
#                 }
#                 result_dict.update(temp_dict)
#                 # print temp_dict
#     return result_dict


def close_connections(cursor):
    cursor.close()
    DB_connector.cnx.close()


cursor = create_connections()

imps_rev_last_5_days(cursor, query_imps_rev_last_days_5, entity_names[0])

result_imps_rev_last_5_days = fetch_data(cursor)

# print result_imps_rev_last_5_days


for i in range(2):
    if i == 0:
        lst2 = [item[2] for item in result_imps_rev_last_5_days]
        avrg_4_days_rev = (sum(lst2[:-1]) / len(lst2[:-1])) / 4
        yesterdays_rev = lst2[-1]
        imps_last_5_days_delta = round(((avrg_4_days_rev / yesterdays_rev) / yesterdays_rev) * 100, 2)
    elif i == 1:
        lst3 = [item[3] for item in result_imps_rev_last_5_days]
        avrg_4_days_imps = (sum(lst3[:-1]) / len(lst3[:-1])) / 4
        yesterdays_imps = lst3[-1]
        rev_last_5_days_delta = round(((avrg_4_days_imps / yesterdays_imps) / yesterdays_imps) * 100, 2)


# cursor = serving_24_hours(cursor, query_serving_24_hours)
#
# result_24_hour_serving = fetch_data(cursor)

close_connections(cursor)
