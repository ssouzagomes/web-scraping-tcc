import requests, json
from requests.models import HTTPError

async def execute(game, cursor, connection):
  try:
    gameSlug = game['catalogNs']['mappings'][0]['pageSlug']

    response = requests.get("https://store-content-ipv4.ak.epicgames.com/api/pt-BR/content/products/"+gameSlug)

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
      platform = addicionalGameInfo['meta']['platform']

    if 'description' in game:
      description = game['description']

    if 'developer' in addicionalGameInfo['meta']:
      developer = addicionalGameInfo['meta']['developer']

    if 'publisher' in addicionalGameInfo['meta']:
      publisher = addicionalGameInfo['meta']['publisher']

    if 'tags' in addicionalGameInfo['meta']:
      genres = addicionalGameInfo['meta']['tags']

    data = {
      'id': game['id'],
      'name': game['title'],
      'game_slug': gameSlug,
      'price': game['currentPrice'],
      'release_date': game['releaseDate'],
      'platform': platform,
      'description': description,
      'developer': developer,
      'publisher': publisher,
      'genres':genres
    }

    print(json.dumps(data, indent=4))
    print("\n")

    # cursor.execute(
    #   """INSERT INTO games (
    #     id, name, game_slug, price, release_date,
    #     platform, description, developer, publisher, genres
    #   ) VALUES (
    #     %s,
    #   );"""
    # )
  except HTTPError as http_error:
    print('HTTP error occurred: %s' %http_error)
  except Exception as error:
    print('Internal error occurred: %s' %error)
