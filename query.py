import DB_connector
from datetime import date, timedelta
from Vars import *


def create_connections():
    cursor = DB_connector.cnx.cursor(buffered=True)
    return cursor


def execute_query(cursor, query, entity_name):
    today = date.today()
    start_date = today - timedelta(5)
    end_date = today - timedelta(1)
    try:
        cursor.execute(query.format(start_date,end_date,entity_name))
        # print query.format(start_date,end_date,entity_name)
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


def convert_to_dict(data,entity_name):
    result_dict = {}
    for i in range(len(data)):
        for ii in range(len(data[i])):
            if data[i][0] == entity_name:
                temp_dict = {
                    data[i][0]:{
                        data[i][1]: {
                            "IMPs": data[i][2],
                            "Rev": data[i][3]
                        }
                    }
                }
                result_dict.update(temp_dict)
                # print temp_dict
    return result_dict

def close_connections(cursor):
    cursor.close()
    DB_connector.cnx.close()


cursor = create_connections()


# execute_query(cursor, query=test)



all_entity_list = []
for entity in range(len(entity_names)):

    execute_query(cursor, test,entity_names[entity])

    result = fetch_data(cursor)

    result_dict = convert_to_dict(result,entity_names[entity])

    all_entity_list.append(result_dict)

print all_entity_list

close_connections(cursor)

