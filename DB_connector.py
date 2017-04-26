import mysql.connector
from Vars import *
from mysql.connector import errorcode
from

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


def create_connection(**args):
    try:
        cnx = mysql.connector.connect(**args)
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


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
print execute_query(cursor=cursor, query=testing)


# for row in cursor:
#     print "{entity_name}, {date_interval}".format(**row)