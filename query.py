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

        cursor.execute(query.format(start_date, end_date, entity_name))
        return cursor
    except Exception as e:
        logging.critical(e)
        raise e


def fetch_data(cursor):
    row = cursor.fetchall()
    if row is None:
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

# imps_rev_last_5_days(cursor, test, entity_names[0])

# ----------------------------- 24 hour serving test --------------
# cursor = serving_24_hours(cursor, query_serving_24_hours)

# result_24_hour_serving = fetch_data(cursor)
#------------------------------------------------------------------
close_connections(cursor)
