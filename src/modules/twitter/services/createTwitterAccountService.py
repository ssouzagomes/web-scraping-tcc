import requests, json
from requests.models import HTTPError

from modules.epic_games.repositories import socialNetworksRepository
from modules.twitter.repositories import twitterAccountsRepository
from modules.twitter.services import createTweetService

async def execute(headers):
  try:
    usernames = await socialNetworksRepository.getAllUsernames()

    pagination_usernames = usernames[:100]
    del usernames[:100]

    pagination_usernames = ','.join(pagination_usernames)

    while len(pagination_usernames) > 0:
      url = ("https://api.twitter.com/2/users/by?usernames=%s" % pagination_usernames +
            "&user.fields=description,location,url,created_at,public_metrics,protected")

      response = requests.get(url, headers=headers)

      if 'data' in json.loads(response.text):
        twitterAccounts = json.loads(response.text)['data']

        await twitterAccountsRepository.create(twitterAccounts)

        twitterAccountIds = []
        twitterAccountUsernames = []

        for twitterAccount in twitterAccounts:
          if(twitterAccount['protected'] == False):
            twitterAccountIds.append(twitterAccount['id'])
            twitterAccountUsernames.append(twitterAccount['username'])

        await createTweetService.execute(twitterAccountIds, twitterAccountUsernames, headers)
      else:
        print("\nUnable to recover twitter accounts.\n")

        pagination_usernames = usernames[:100]
        del usernames[:100]

        pagination_usernames = ','.join(pagination_usernames)

  except HTTPError as http_error:
    print('HTTP error occurred: %s' %http_error)
  except Exception as error:
    print('Internal error occurred: %s' %error)
