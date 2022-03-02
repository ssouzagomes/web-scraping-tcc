import requests
import json
from requests.models import HTTPError

from modules.epic_games import insertInDatabase


async def execute(game):
  try:
    gameSlug = game['catalogNs']['mappings'][0]['pageSlug']

    url = "https://store-content-ipv4.ak.epicgames.com/api/en-US/content/products/"+gameSlug

    response = requests.get(url)

    addicionalGameInfo = json.loads(response.text)['pages'][0]['data']

    file = open("addicional-info-game.json","w")
    file.write(response.text)
    file.close()

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

    socialNetworks = addicionalGameInfo['socialLinks']

    if '_type' in socialNetworks:
      del socialNetworks['_type']
    if 'title' in socialNetworks:
      del socialNetworks['title']
    if 'linkHomepage' in socialNetworks:
      del socialNetworks['linkHomepage']

    formattedSocialNetworks = {}

    for key in socialNetworks:
      if socialNetworks[key] != '':
        formattedSocialNetworks[key] = socialNetworks[key]

    await insertInDatabase.execute(formattedGame, formattedSocialNetworks)

  except HTTPError as http_error:
    print('HTTP error occurred: %s' % http_error)
  except Exception as error:
    print('Internal error occurred: %s' % error)
