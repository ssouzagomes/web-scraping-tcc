import psycopg2

from configparser import ConfigParser

# create a parser
parser = ConfigParser()
# read config file
parser.read('database.ini')

print(parser.has_section('postgresql'))

# Connect to your postgres DB
# connection = psycopg2.connect("host=localhost user=postgres dbname=tcc password=docker")

# Open a cursor to perform database operations
# cursor = connection.cursor()

# Execute a query
# cur.execute("SELECT * FROM my_data")

# Retrieve query results
# records = cursor.fetchall()