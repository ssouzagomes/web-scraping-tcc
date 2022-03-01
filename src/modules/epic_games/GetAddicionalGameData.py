import requests
from requests.models import HTTPError

async def execute():
  try:
    response = requests.get("https://store-content-ipv4.ak.epicgames.com/api/pt-BR/content/products/not-tonight-2")

    file = open("addicional-info-game.json","w")

    file.write(response.text)

    file.close()
  except HTTPError as http_error:
    print('HTTP error occurred: %s' %http_error)
  except Exception as error:
    print('Internal error occurred: %s' %error)