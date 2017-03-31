import DB_connector
from Vars import *

def create_connections():
  cursor = DB_connector.cnx.cursor(buffered=True)
  return cursor

def execute_query(cursor,query):
  try:
    cursor.execute(query)
  except Exception as e:
    raise e # TODO add a log level error with HIGH priority.
  return cursor

def fetch_data(cursor):
  row = cursor.fetchone()
  if row is None: # TODO: add a logger level error with HIGH priority.
    print 'No data was returned by query' 
  elif row is not None:
    while row is not None:
      query_response = list(row)
      row = cursor.fetchone()
    return query_response

def close_connections(cursor):
  cursor.close()
  DB_connector.cnx.close()

cursor = create_connections()
execute_query(cursor,query=test)
# execute_query(cursor,min_time_stamp)
Placeholder = fetch_data(cursor)
close_connections(cursor)