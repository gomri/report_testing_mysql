import DB_connector
import json
from Vars import *


def create_connections():
    cursor = DB_connector.cnx.cursor(buffered=True)
    return cursor


def execute_query(cursor, query):
    try:
        cursor.execute(query)
    except Exception as e:
        raise e  # TODO add a log level error with HIGH priority.
    return cursor


def fetch_data(cursor):
    row = cursor.fetchall()
    if row is None:  # TODO: add a logger level error with HIGH priority.
        print 'No data was returned by query'
    elif row is not None:
        while row is not None:
            query_response = list(row)
            row = cursor.fetchone()
        return query_response


def convert_to_dict(data):
    OpenX_dict = {}
    for i in range(len(data)):
        for ii in range(len(data[i])):
            if data[i][0] == "OpenX":
                temp_dict = {
                    data[i][1]: {
                        "IMPs": data[i][2],
                        "Rev": data[i][3]
                    }
                }
                OpenX_dict.update(temp_dict)
    return OpenX_dict


# def convert_to_json(data):
#     d = json.dumps(data)
#     return d

def close_connections(cursor):
    cursor.close()
    DB_connector.cnx.close()


cursor = create_connections()
execute_query(cursor, query=test)
# execute_query(cursor,min_time_stamp)
result = fetch_data(cursor)
result_dict = convert_to_dict(result)
close_connections(cursor)
