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

  option = input("1 - Request games data\n" +
                 "2 - Request games reviews\n" +
                 "3 - Request twitter users data\n\n")

  # if option == "1":
  #   cursor, connection = await DatabaseConnection.execute()
  #   await CreateSchema.execute(cursor, connection)

  if option == "1":
    await createGameService.execute()

  elif option == "2":
    await createGameReviewService.execute()

  elif option == "3":
    await createTwitterAccountService.execute(TwitterAuthenticate.headers)

  else:
    print('Invalid option!')

asyncio.run(__main__())