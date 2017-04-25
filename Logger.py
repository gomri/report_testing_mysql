import logging

# Creates the logger and sets it's logs format
FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='logs.log', level=logging.DEBUG, format=FORMAT)