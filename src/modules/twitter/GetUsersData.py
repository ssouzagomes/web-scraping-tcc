import requests, json, csv
from requests.models import HTTPError

from modules.twitter import GetTweetsData

async def execute(headers):
  try:
    usernames = 'EpicGames'

    url = ("https://api.twitter.com/2/users/by?usernames=%s" % usernames +
    "&user.fields=description,location,url,created_at,public_metrics,protected")

    response = requests.get(url, headers=headers)

    users = json.loads(response.text)['data']

    with open('users.tsv', 'wt') as out_file:
      for user in users:
        for column in user:
          if(column == 'public_metrics'):
            tsv_writer = csv.writer(out_file, delimiter='\t')
            tsv_writer.writerow(['followers_count', user[column]['followers_count']])

            tsv_writer = csv.writer(out_file, delimiter='\t')
            tsv_writer.writerow(['following_count', user[column]['following_count']])
          else:
            tsv_writer = csv.writer(out_file, delimiter='\t')
            tsv_writer.writerow([column, user[column]])

    user_ids = []

    for user in users:
      if(user['protected'] == False):
        user_ids.append(user['id'])

    await GetTweetsData.execute(user_ids, headers)
    
  except HTTPError as http_error:
    print('HTTP error occurred: %s' %http_error)
  except Exception as error:
    print('Internal error occurred: %s' %error)
