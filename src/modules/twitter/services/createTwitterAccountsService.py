import requests, json
from requests.models import HTTPError

from modules.epic_games.repositories import socialNetworksRepository
from modules.twitter.repositories import twitterAccountsRepository
from modules.twitter.services import createTweetsService

async def execute(headers):
  try:
    usernames = await socialNetworksRepository.getAllUsernames()

    url = ("https://api.twitter.com/2/users/by?usernames=%s" % usernames +
    "&user.fields=description,location,url,created_at,public_metrics,protected")

    response = requests.get(url, headers=headers)

    twitterAccounts = json.loads(response.text)['data']

    # file = open("users.json","w")
    # file.write(response.text)
    # file.close()

    await twitterAccountsRepository.create(twitterAccounts)

    twitterAccountIds = []
    twitterAccountUsernames = []

    for twitterAccount in twitterAccounts:
      if(twitterAccount['protected'] == False):
        twitterAccountIds.append(twitterAccount['id'])
        twitterAccountUsernames.append(twitterAccount['username'])

    await createTweetsService.execute(twitterAccountIds, twitterAccountUsernames, headers)

  except HTTPError as http_error:
    print('HTTP error occurred: %s' %http_error)
  except Exception as error:
    print('Internal error occurred: %s' %error)
