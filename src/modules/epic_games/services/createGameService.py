import requests, json
from datetime import date
from requests.models import HTTPError

from modules.epic_games.repositories import gameRepository
from modules.epic_games.services import createSocialNetworkService
from modules.epic_games.services import createNecessaryHardwareService

async def execute():
  try:
    dateNow = date.today()

    games_response = requests.get('https://store.epicgames.com/graphql?operationName=' +
      'searchStoreQuery&variables={"allowCountries":"US",' +
      '"category":"games/edition/base|software/edition/base|editors|bundles/games",'+
      '"count":1000,"country":"US","locale":"en-US","releaseDate":"[,%sT17:50:56.950Z]",' %dateNow + 
      '"sortBy":"releaseDate","sortDir":"DESC"}&extensions={"persistedQuery":'+
      '{"version":1,"sha256Hash":"4bebe12f9eab12438766fb5971b0bc54422ba81954539f294ec23b0a29ff92ad"}}'
    )

    games_json = json.loads(games_response.text)

    file = open("games.json","w")
    file.write(games_response.text)
    file.close()

    if 'game' in games_response.text:
      games = games_json['data']['Catalog']['searchStore']['elements']

      print(len(games))

      for game in games:
        gameSlug = game['catalogNs']['mappings'][0]['pageSlug']

        addicional_info_url = "https://store-content-ipv4.ak.epicgames.com/api/en-US/content/products/"+gameSlug

        addicional_info_response = requests.get(addicional_info_url)

        file = open("specifications.json","w")
        file.write(addicional_info_response.text)
        file.close()

        platform = ''
        genres = ''

        if 'pages' in json.loads(addicional_info_response.text):
          addicionalGameInfo = json.loads(addicional_info_response.text)['pages'][0]['data']

          if 'data' in json.loads(addicional_info_response.text)['pages'][0]:
            if 'platform' in addicionalGameInfo['meta']:
              platform = ','.join(addicionalGameInfo['meta']['platform'])

            if 'tags' in addicionalGameInfo['meta']:
              genres = ','.join(addicionalGameInfo['meta']['tags'])

            formattedGame = {
              'id': game['id'],
              'name': game['title'],
              'game_slug': gameSlug,
              'price': game['currentPrice'],
              'release_date': game['releaseDate'],
              'platform': platform,
              'description': game['description'],
              'developer': game['developerDisplayName'],
              'publisher': game['publisherDisplayName'],
              'genres': genres
            }

            await gameRepository.create(formattedGame)

            await createSocialNetworkService.execute(formattedGame, addicionalGameInfo)

            await createNecessaryHardwareService.execute(addicionalGameInfo, gameSlug)
        else:
          addicional_info_url = "https://store.epicgames.com/pt-BR/p/"+gameSlug

          addicional_info_response = requests.get(addicional_info_url)

          file = open("specifications.html","w")
          file.write(addicional_info_response.text)
          file.close()

          formattedGame = {
            'id': game['id'],
            'name': game['title'],
            'game_slug': gameSlug,
            'price': game['currentPrice'],
            'release_date': game['releaseDate'],
            'platform': platform,
            'description': game['description'],
            'developer': game['developerDisplayName'],
            'publisher': game['publisherDisplayName'],
            'genres': genres
          }

          await gameRepository.create(formattedGame)
    else:
      print('\nUnable to recover game data. Try again!\n')

          
  except HTTPError as http_error:
    print('HTTP error occurred: %s' %http_error)
  except Exception as error:
    print('Internal error occurred: %s' %error)
