import sys
import asyncio

sys.dont_write_bytecode = True

from shared.migrations import create_schema
from config import database_connection, twitter_authenticate

from modules.twitter import get_users_data
from modules.epic_games import get_games_data

print('### CHOOSE ONE OPTION ###\n')

option = input("1 - Create schema\n" +
               "2 - Get twitter users data\n" +
               "3 - Get games data\n\n")

if option == "1":
  cursor, connection = asyncio.run(database_connection.execute())
  asyncio.run(create_schema.execute(cursor, connection))

elif option == "2":
  asyncio.run(get_users_data.execute(twitter_authenticate.headers))

elif option == "3":
  asyncio.run(get_games_data.execute())

else:
  print('Opção inválida!')