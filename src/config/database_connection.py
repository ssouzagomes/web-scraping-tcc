import psycopg2

from configparser import ConfigParser

# create a parser
config = ConfigParser()

# read config file
config.read('environment.ini')

# Connect to your postgres DB
host = config['postgresql']['host']
user = config['postgresql']['user']
dbname = config['postgresql']['dbname']
password = config['postgresql']['password']

connection = psycopg2.connect("host="+host+" user="+user+" dbname="+dbname+" password="+password)

# Open a cursor to perform database operations
# cursor = connection.cursor()

# Execute a query
# cursor.execute("SELECT * FROM my_data")

# Retrieve query results
# records = cursor.fetchall()