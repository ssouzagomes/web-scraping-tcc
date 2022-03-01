import sys
import asyncio

sys.dont_write_bytecode = True

from shared.migrations import CreateSchema
from config import DatabaseConnection, TwitterAuthenticate

from modules.twitter import GetUsersData
from modules.epic_games import GetGamesData

print('### CHOOSE ONE OPTION ###\n')

option = input("1 - Create schema\n" +
               "2 - Get games data\n" +
               "3 - Get previews games\n" +
               "4 - Get twitter users data\n\n")

if option == "1":
  cursor, connection = asyncio.run(DatabaseConnection.execute())
  asyncio.run(CreateSchema.execute(cursor, connection))

elif option == "2":
  asyncio.run(GetGamesData.execute())

elif option == "3":
  print('previews')
  # asyncio.run(GetGamesData.execute())

elif option == "4":
  asyncio.run(GetUsersData.execute(TwitterAuthenticate.headers))

else:
  print('Opção inválida!')