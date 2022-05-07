import requests, json, csv
from requests.models import HTTPError

from modules.epic_games.repositories import socialNetworksRepository
from modules.twitter.repositories import twitterAccountsRepository
from modules.twitter.services import createTweetService

async def execute(headers):
  try:
    twitter_accounts_file = open('twitter_accounts.csv', 'w')
    twitter_accounts_writer = csv.writer(twitter_accounts_file)
    header_twitter_accounts_file = (
      'id', 'name', 'username', 'bio', 'location', 'website', 'join_date', 'following', 'followers', 'fk_game_id'
    )
    twitter_accounts_writer.writerow(header_twitter_accounts_file)

    usernames = await socialNetworksRepository.getAllUsernames()

    if len(usernames) > 0 and len(usernames) < 100:
      pagination_usernames = usernames
      usernames = []
    else:
      pagination_usernames = usernames[:100]
      del usernames[:100]

    while len(pagination_usernames) > 0:
      formatUsernames = ','.join(pagination_usernames)

      url = ("https://api.twitter.com/2/users/by?usernames=%s" % formatUsernames +
            "&user.fields=description,location,url,created_at,public_metrics,protected")

      response = requests.get(url, headers=headers)

      if 'data' in json.loads(response.text):
        twitterAccounts = json.loads(response.text)['data']

        await twitterAccountsRepository.create(twitterAccounts, twitter_accounts_writer)

        twitterAccountIds = []
        twitterAccountUsernames = []

        for twitterAccount in twitterAccounts:
          if(twitterAccount['protected'] == False):
            twitterAccountIds.append(twitterAccount['id'])
            twitterAccountUsernames.append(twitterAccount['username'])

        await createTweetService.execute(twitterAccountIds, headers)

      else:
        print("\nUnable to recover twitter accounts.\n")

        if len(usernames) > 0 and len(usernames) < 100:
          pagination_usernames = usernames
          usernames = []
        else:
          pagination_usernames = usernames[:100]
          del usernames[:100]

      if len(usernames) > 0 and len(usernames) < 100:
        pagination_usernames = usernames
        usernames = []
      else:
        pagination_usernames = usernames[:100]
        del usernames[:100]
      
    twitter_accounts_file.close()

  except HTTPError as http_error:
    print('HTTP error occurred: %s' %http_error)
  except Exception as error:
    print('Internal error occurred: %s' %error)
