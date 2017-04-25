import mysql.connector
from mysql.connector import errorcode
from Logger import *

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
