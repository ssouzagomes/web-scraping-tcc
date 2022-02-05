import requests, json, csv
from requests.models import HTTPError

async def tweets_timeline(user_ids, headers):
  for user_id in user_ids:
    
    url = ("https://api.twitter.com/2/users/%s/tweets?max_results=10" % user_id +
      "&expansions=attachments.media_keys,in_reply_to_user_id" +
      "&tweet.fields=public_metrics,created_at" +
      "&media.fields=preview_image_url,url")

    response = requests.get(url, headers=headers)

    if('data' in json.loads(response.text)):
      tweets = json.loads(response.text)['data']

      with open(user_id+'tweets.tsv', 'wt') as out_file:
        for tweet in tweets:
          for column in tweet:
            tsv_writer = csv.writer(out_file, delimiter='\t')
            tsv_writer.writerow([column, tweet[column]])


async def __main__(headers):
  try:
    usernames = 'EpicGames'

    url = ("https://api.twitter.com/2/users/by?usernames=%s" % usernames +
    "&user.fields=description,location,url,created_at,public_metrics,protected")

    response = requests.get(url, headers=headers)
    print(response)

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

    await tweets_timeline(user_ids, headers)
    
  except HTTPError as http_error:
    print('HTTP error occurred: %s' %http_error)
  except Exception as error:
    print('Internal error occurred: %s' %error)

# asyncio.run(main())