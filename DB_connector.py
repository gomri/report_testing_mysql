import mysql.connector
from mysql.connector import errorcode

try:
  cnx = mysql.connector.connect(user='omrig',
  							  password='zUAv5hsG',
                              host='54.208.36.131',
                              database='onetag')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  print 'connection successful'

  