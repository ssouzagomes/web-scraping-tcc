import requests, json
from requests.models import HTTPError

async def execute(twitterAccountIds, headers):
  try:
    for twitterAccountId in twitterAccountIds:
      url = ("https://api.twitter.com/2/users/%s/tweets?max_results=5" % twitterAccountId +
        "&expansions=attachments.media_keys" +
        "&tweet.fields=public_metrics,created_at" +
        "&media.fields=media_key,preview_image_url,type,url")

      response = requests.get(url, headers=headers)

      if('data' in json.loads(response.text)):
        tweets = json.loads(response.text)['data']

        medias = json.loads(response.text)['includes']['media']

        for tweet in tweets:
          publicMetrics = tweet['public_metrics']

          formattedTweet = {
            'text': tweet['text'],
            'timestamp': tweet['created_at'],
            'quantity_likes': publicMetrics['like_count'],
            'quantity_retweets': publicMetrics['retweet_count'],
            'quantity_quotes': publicMetrics['quote_count'],
            'quantity_replys': publicMetrics['reply_count'],
            'twitter_account_id': twitterAccountId,
            'url_media': ()
          }

          if 'attachments' in tweet:
            if 'media_keys' in tweet['attachments']:
              media_keys = tweet['attachments']['media_keys']

              for media in medias:
                for media_key in media_keys:
                  if media['media_key'] == media_key and 'preview_image_url' in media:
                    formattedTweet['url_media'] += (media['preview_image_url'],)

          if len(formattedTweet['url_media']) > 0:
            formattedTweet['url_media'] = ','.join(formattedTweet['url_media'])
          else:
            formattedTweet['url_media'] = ''

          print(json.dumps(formattedTweet, indent=4))
          print('\n')

        file = open("tweets.json","w")
        file.write(response.text)
        file.close()

  except HTTPError as http_error:
    print('HTTP error occurred: %s' %http_error)
  except Exception as error:
    print('Internal error occurred: %s' %error)
