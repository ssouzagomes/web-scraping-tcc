import sys
import asyncio

sys.dont_write_bytecode = True

from shared.migrations import CreateSchema
from config import DatabaseConnection, TwitterAuthenticate

from modules.twitter.services import getUsersService
from modules.epic_games import getGames

async def __main__():
  print('### CHOOSE ONE OPTION ###\n')

  option = input("1 - Create schema\n" +
                "2 - Get games data\n" +
                "3 - Get previews games\n" +
                "4 - Get twitter users data\n\n")

  if option == "1":
    cursor, connection = await DatabaseConnection.execute()
    await CreateSchema.execute(cursor, connection)

  elif option == "2":
    await getGames.execute()

  elif option == "3":
    print('previews')
    # await GetGamesData.execute()

  elif option == "4":
    await getUsersService.execute(TwitterAuthenticate.headers)

  else:
    print('Opção inválida!')

asyncio.run(__main__())