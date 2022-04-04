import sys
import asyncio

sys.dont_write_bytecode = True

from shared.migrations import CreateSchema
from config import DatabaseConnection, TwitterAuthenticate

from modules.twitter.services import createTwitterAccountService
from modules.epic_games.services import createGameService
from modules.open_critic.services import createGameReviewService

async def __main__():
  print('### CHOOSE ONE OPTION ###\n')

  option = input("1 - Create schema\n" +
                 "2 - Request games data\n" +
                 "3 - Request games reviews\n" +
                 "4 - Request twitter users data\n\n")

  if option == "1":
    cursor, connection = await DatabaseConnection.execute()
    await CreateSchema.execute(cursor, connection)

  elif option == "2":
    await createGameService.execute()

  elif option == "3":
    await createGameReviewService.execute()

  elif option == "4":
    await createTwitterAccountService.execute(TwitterAuthenticate.headers)

  else:
    print('Opção inválida!')

asyncio.run(__main__())