import requests, json, asyncio, csv
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

  followers = json.loads(response.text)['data']

  print(followers)


async def liked_tweets(id):
  url = "https://api.twitter.com/2/users/"+id+"/liked_tweets"

  response = requests.get(url, headers=headers)

  liked = json.loads(response.text)['data']

  print(liked)


async def main():
  try:
    url = "https://api.twitter.com/2/users/by?usernames=EpicGames&user.fields=description,location,url,created_at"

    response = requests.get(url, headers=headers)

    users = json.loads(response.text)['data']

    with open('users.tsv', 'wt') as out_file:
      for user in users:
        for column in user:
          tsv_writer = csv.writer(out_file, delimiter='\t')
          tsv_writer.writerow([column, user[column]])

    userId = users[0]['id']

    # await get_followers(userId)
    # await liked_tweets(id)
    
  except HTTPError as http_error:
    print('HTTP error occurred: ' + http_error)
  except Exception as error:
    print('Internal error occurred: ' + error)

asyncio.run(main())