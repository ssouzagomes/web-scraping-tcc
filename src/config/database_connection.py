import psycopg2

from configparser import ConfigParser

async def execute():
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
  cursor = connection.cursor()

  return cursor, connection