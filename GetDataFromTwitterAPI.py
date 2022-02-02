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

async def tweets_timeline(user_ids):
  for user_id in user_ids:
    url = "https://api.twitter.com/2/users/"+user_id+"/tweets"

    response = requests.get(url, headers=headers)

    if('data' in json.loads(response.text)):
      tweets = json.loads(response.text)['data']

      with open(user_id+'tweets.tsv', 'wt') as out_file:
        for tweet in tweets:
          for column in tweet:
            tsv_writer = csv.writer(out_file, delimiter='\t')
            tsv_writer.writerow([column, tweet[column]])


async def main():
  try:
    usernames = 'EpicGames,samuel_ufop'

    url = "https://api.twitter.com/2/users/by?usernames="+usernames+"&user.fields=description,location,url,created_at,public_metrics,protected"

    response = requests.get(url, headers=headers)

    users = json.loads(response.text)['data']

    with open('users.tsv', 'wt') as out_file:
      for user in users:
        for column in user:
          tsv_writer = csv.writer(out_file, delimiter='\t')
          tsv_writer.writerow([column, user[column]])

    user_ids = []

    for user in users:
      if(user['protected'] == False):
        user_ids.append(user['id'])

    await tweets_timeline(user_ids)
    
  except HTTPError as http_error:
    print('HTTP error occurred: ' + http_error)
  except Exception as error:
    print('Internal error occurred: ' + error)

asyncio.run(main())