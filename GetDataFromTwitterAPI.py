import requests, json, asyncio
from requests.models import HTTPError
from requests.structures import CaseInsensitiveDict

API_KEY = "Z1GoRostJxEhk9sQEk3O3KJ3O"
API_KEY_SECRET = "uU9Q4fUnHfr11s5kjwVprDKFQ11C8tXLDlyJ296MEGxo8h7Ts2"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAANxNUwEAAAAAhwrD3%2B%2FVj7FDrW4AQiFtuSyBTlY%3D0UBvwyDCzmrGhHHKgciQtj8r6GXJ4JLpbmzIp2hGJ5mSNwmntB"
ACCESS_TOKEN = "1450238995787653121-bMdBxW4BA8C5ZlW50kixIthaQ0PjUp"
ACCESS_TOKEN_SECRET = "OAnyAmQhNE3pysuSPaLuFhwi2oFfuL776xNoqnzsEgcZt"

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Authorization"] = "Bearer " + BEARER_TOKEN

async def get_followers(id):
  url = "https://api.twitter.com/2/users/"+id+"/followers"

  response = requests.get(url, headers=headers)

  output = json.loads(response.text)


async def liked_twittes(id):
  url = "https://api.twitter.com/2/users/"+id+"/liked_tweets"

  response = requests.get(url, headers=headers)

  output = json.loads(response.text)

  print(output['data'])


async def main():
  try:
    url = "https://api.twitter.com/2/users/by/username/EpicGames"

    response = requests.get(url, headers=headers)

    output = json.loads(response.text)

    id = output['data']['id']

    await liked_twittes(id)
    await get_followers(id)

    
  except HTTPError as http_error:
    print('HTTP error occurred: ' + http_error)
  except Exception as error:
    print('Internal error occurred: ' + error)

asyncio.run(main())