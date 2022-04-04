import requests, json
from requests.models import HTTPError

from modules.epic_games.repositories import gameRepository
from modules.epic_games.services import createSocialNetworkService

async def execute():
  try:
    games_url = ('https://www.epicgames.com/graphql?operationName=' +
    'searchStoreQuery&variables={"allowCountries":"US",' +
    '"category":"games/edition/base|software/edition/base|editors|bundles/games",'+
    '"count":5,"country":"US","locale":"en-US","releaseDate":"[,2022-02-19T17:50:56.950Z]",'+
    '"sortBy":"releaseDate","sortDir":"ASC"}&extensions={"persistedQuery":'+
    '{"version":1,"sha256Hash":"6e7c4dd0177150eb9a47d624be221929582df8648e7ec271c821838ff4ee148e"}}')

    games_response = requests.get(games_url)

    games = json.loads(games_response.text)['data']['Catalog']['searchStore']['elements']

    for game in games:
      gameSlug = game['catalogNs']['mappings'][0]['pageSlug']

      addicional_info_url = "https://store-content-ipv4.ak.epicgames.com/api/en-US/content/products/"+gameSlug

      addicional_info_response = requests.get(addicional_info_url)

      addicionalGameInfo = json.loads(addicional_info_response.text)['pages'][0]['data']

      platform = ''
      description = ''
      developer = ''
      publisher = ''
      genres = ''

      if 'platform' in addicionalGameInfo['meta']:
        platform = ','.join(addicionalGameInfo['meta']['platform'])

      if 'description' in game:
        description = game['description']

      if 'developer' in addicionalGameInfo['meta']:
        developer = ','.join(addicionalGameInfo['meta']['developer'])

      if 'publisher' in addicionalGameInfo['meta']:
        publisher = ','.join(addicionalGameInfo['meta']['publisher'])

      if 'tags' in addicionalGameInfo['meta']:
        genres = ','.join(addicionalGameInfo['meta']['tags'])

      formattedGame = {
        'id': game['id'],
        'name': game['title'],
        'game_slug': gameSlug,
        'price': game['currentPrice'],
        'release_date': game['releaseDate'],
        'platform': platform,
        'description': description,
        'developer': developer,
        'publisher': publisher,
        'genres': genres
      }

      await gameRepository.create(formattedGame)

      await createSocialNetworkService.execute(formattedGame, addicionalGameInfo)

    print("\nRecord inserted successfully into games table.\n")
          
  except HTTPError as http_error:
    print('HTTP error occurred: %s' %http_error)
  except Exception as error:
    print('Internal error occurred: %s' %error)
