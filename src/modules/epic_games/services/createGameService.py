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
      '"count":10,"country":"US","locale":"en-US","releaseDate":"[,%sT00:00:00.950Z]",' %dateNow + 
      '"sortBy":"releaseDate","sortDir":"ASC"}&extensions={"persistedQuery":'+
      '{"version":1,"sha256Hash":"4bebe12f9eab12438766fb5971b0bc54422ba81954539f294ec23b0a29ff92ad"}}'
    )

    games_json = json.loads(games_response.text)

    if 'game' in games_response.text:
      games = games_json['data']['Catalog']['searchStore']['elements']

      formattedGames = []
      formattedAddicionalGameInfos = []

      for game in games:
        gameSlug = game['catalogNs']['mappings'][0]['pageSlug']

        addicional_info_url = "https://store-content-ipv4.ak.epicgames.com/api/en-US/content/products/"+gameSlug

        addicional_info_response = requests.get(addicional_info_url)

        platform = ''
        genres = ''
        developer = ''
        publisher = ''

        addicional_info_json = json.loads(addicional_info_response.text)

        if 'pages' in addicional_info_json:
          if 'data' in addicional_info_json['pages'][0]:
            addicionalGameInfo = addicional_info_json['pages'][0]['data']

            if 'platform' in addicionalGameInfo['meta']:
              platform = ','.join(addicionalGameInfo['meta']['platform'])

            if 'tags' in addicionalGameInfo['meta']:
              genres = ','.join(addicionalGameInfo['meta']['tags'])

            if 'developer' in addicionalGameInfo['meta']:
              developer = ','.join(addicionalGameInfo['meta']['developer'])

            if 'publisher' in addicionalGameInfo['meta']:
              publisher = ','.join(addicionalGameInfo['meta']['publisher'])

            formattedGame = {
              'id': game['id'],
              'name': game['title'],
              'game_slug': gameSlug,
              'price': game['currentPrice'],
              'release_date': game['releaseDate'],
              'platform': platform,
              'description': game['description'],
              'developer': developer,
              'publisher': publisher,
              'genres': genres
            }

            formattedGames.append(formattedGame)

            formattedAddicionalGameInfo = {
              'socialNetworks': addicionalGameInfo['socialLinks'],
              'gameId': formattedGame['id']
            }

            formattedAddicionalGameInfos.append(formattedAddicionalGameInfo)
            # await createNecessaryHardwareService.execute(addicionalGameInfo, gameSlug)

          elif 'data' in addicional_info_json['pages'][1]:
            addicionalGameInfo = addicional_info_json[1]['data']

            if 'platform' in addicionalGameInfo['meta']:
              platform = ','.join(addicionalGameInfo['meta']['platform'])

            if 'tags' in addicionalGameInfo['meta']:
              genres = ','.join(addicionalGameInfo['meta']['tags'])

            if 'developer' in addicionalGameInfo['meta']:
              developer = ','.join(addicionalGameInfo['meta']['developer'])

            if 'publisher' in addicionalGameInfo['meta']:
              publisher = ','.join(addicionalGameInfo['meta']['publisher'])

            formattedGame = {
              'id': game['id'],
              'name': game['title'],
              'game_slug': gameSlug,
              'price': game['currentPrice'],
              'release_date': game['releaseDate'],
              'platform': platform,
              'description': game['description'],
              'developer': developer,
              'publisher': publisher,
              'genres': genres
            }

            formattedGames.append(formattedGame)

            formattedAddicionalGameInfo = {
              'socialNetworks': addicionalGameInfo['socialLinks'],
              'gameId': formattedGame['id']
            }

            formattedAddicionalGameInfos.append(formattedAddicionalGameInfo)

            # await createNecessaryHardwareService.execute(addicionalGameInfo, gameSlug)

        else:
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

          formattedGames.append(formattedGame)

      await gameRepository.create(formattedGames)
      await createSocialNetworkService.execute(formattedAddicionalGameInfos)
    else:
      print('\nUnable to recover game data. Try again!\n')
          
  except HTTPError as http_error:
    print('HTTP error occurred: %s' %http_error)
  except Exception as error:
    print('Internal error occurred: %s' %error)
