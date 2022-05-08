import requests, json, csv
from datetime import date
from requests.models import HTTPError

from modules.epic_games.repositories import gameRepository
from modules.epic_games.services import createSocialNetworkService
from modules.epic_games.services import createNecessaryHardwareService

async def execute():
  try:
    dateNow = date.today()

    games_file = open('games.csv', 'w')
    games_writer = csv.writer(games_file)
    header_games_file = (
      'id', 'name', 'game_slug', 'price', 'release_date', 'platform', 'description', 'developer', 'publisher', 'genres'
    )
    games_writer.writerow(header_games_file)

    necessary_hardware_file = open('necessary_hardware.csv', 'w')
    necessary_hardware_writer = csv.writer(necessary_hardware_file)
    header_necessary_hardware_file = (
      'id', 'operacional_system', 'processor', 'memory', 'graphics', 'fk_game_id'
    )
    necessary_hardware_writer.writerow(header_necessary_hardware_file)
    
    games_response = requests.get('https://store.epicgames.com/graphql?operationName=' +
      'searchStoreQuery&variables={"allowCountries":"US",' +
      '"category":"games/edition/base|software/edition/base|editors|bundles/games",'+
      '"count":1000,"country":"US","locale":"en-US","releaseDate":"[,%sT00:00:00.950Z]",' %dateNow + 
      '"sortBy":"releaseDate","sortDir":"ASC"}&extensions={"persistedQuery":'+
      '{"version":1,"sha256Hash":"4bebe12f9eab12438766fb5971b0bc54422ba81954539f294ec23b0a29ff92ad"}}'
    )

    games_json = json.loads(games_response.text)

    if 'game' in games_response.text:
      games = games_json['data']['Catalog']['searchStore']['elements']

      print(len(games))

      formattedGames = []
      formattedAddicionalGameInfos = []
      addicionalGameInfos = []
      gameIds = []

      for game in games:
        if game['catalogNs']['mappings'] != None:
          if len(game['catalogNs']['mappings']) > 0:
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
                addicionalGameInfos.append(addicionalGameInfo)
                gameIds.append(game['id'])


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
                addicionalGameInfos.append(addicionalGameInfo)
                gameIds.append(game['id'])

        else:
          formattedGame = {
            'id': game['id'],
            'name': game['title'],
            'game_slug': game['productSlug'] or '',
            'price': game['currentPrice'],
            'release_date': game['releaseDate'],
            'platform': '',
            'description': game['description'],
            'developer': game['developerDisplayName'] or '',
            'publisher': game['publisherDisplayName'],
            'genres': ''
          }

          formattedGames.append(formattedGame)

      await gameRepository.create(formattedGames, games_writer)
      await createSocialNetworkService.execute(formattedAddicionalGameInfos)
      await createNecessaryHardwareService.execute(addicionalGameInfos, gameIds, necessary_hardware_writer)

      games_file.close()
      necessary_hardware_file.close()
    else:
      print('\nUnable to recover game data. Try again!\n')
          
  except HTTPError as http_error:
    print('HTTP error occurred: %s' %http_error)
  except Exception as error:
    print('Internal error occurred: %s' %error)
