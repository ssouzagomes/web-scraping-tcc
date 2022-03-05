import requests, json
from requests.models import HTTPError

from modules.epic_games import getAddicionalGameInfo

async def execute():
  try:
    response = requests.get('https://www.epicgames.com/graphql?operationName=' +
    'searchStoreQuery&variables={"allowCountries":"US",' +
    '"category":"games/edition/base|software/edition/base|editors|bundles/games",'+
    '"count":3,"country":"US","locale":"en-US","releaseDate":"[,2022-02-19T17:50:56.950Z]",'+
    '"sortBy":"releaseDate","sortDir":"ASC"}&extensions={"persistedQuery":'+
    '{"version":1,"sha256Hash":"6e7c4dd0177150eb9a47d624be221929582df8648e7ec271c821838ff4ee148e"}}')

    games = json.loads(response.text)['data']['Catalog']['searchStore']['elements']

    # file = open("game.json","w")
    # file.write(response.text)
    # file.close()

    for game in games:
      await getAddicionalGameInfo.execute(game)

    print("\nRecord inserted successfully into games table.\n")
          
  except HTTPError as http_error:
    print('HTTP error occurred: %s' %http_error)
  except Exception as error:
    print('Internal error occurred: %s' %error)
