import requests
from requests.models import HTTPError

async def execute(game):
  try:
    response = requests.get("https://store-content-ipv4.ak.epicgames.com/api/pt-BR/content/products/assassins-creed-1")

    print(game['title'])


    file = open("addicional-info-game.json","w")

    file.write(response.text)

    file.close()
  except HTTPError as http_error:
    print('HTTP error occurred: %s' %http_error)
  except Exception as error:
    print('Internal error occurred: %s' %error)