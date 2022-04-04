import requests, json
from requests.models import HTTPError

from modules.twitter.repositories import tweetRepository

async def execute(twitterAccountIds, twitterAccountUsernames, headers):
  try:
    for index, twitterAccountId in enumerate(twitterAccountIds):
      url = ("https://api.twitter.com/2/users/%s/tweets?max_results=5" % twitterAccountId +
        "&expansions=attachments.media_keys" +
        "&tweet.fields=public_metrics,created_at,in_reply_to_user_id" +
        "&media.fields=media_key,preview_image_url,type,url")

      response = requests.get(url, headers=headers)

      file = open("tweets.json","w")
      file.write(response.text)
      file.close()

      if('data' in json.loads(response.text)):
        tweets = json.loads(response.text)['data']

        medias = []
        haveMedias = False

        if 'includes' in json.loads(response.text):
          if 'media' in json.loads(response.text)['includes']:
            medias = json.loads(response.text)['includes']['media']
            haveMedias = True

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

              if haveMedias == True:
                for media in medias:
                  for media_key in media_keys:
                    if media['media_key'] == media_key and 'preview_image_url' in media:
                      formattedTweet['url_media'] += (media['preview_image_url'],)

          if len(formattedTweet['url_media']) > 0:
            formattedTweet['url_media'] = ','.join(formattedTweet['url_media'])
          else:
            formattedTweet['url_media'] = ''

          await tweetRepository.create(formattedTweet, twitterAccountUsernames[index])

      # while ('next_token' in json.loads(response.text)['meta']):
      #   next_token = json.loads(response.text)['meta']['next_token']

      #   url = ("https://api.twitter.com/2/users/%s/tweets?max_results=100" % twitterAccountId +
      #   "&expansions=attachments.media_keys" +
      #   "&tweet.fields=public_metrics,created_at" +
      #   "&media.fields=media_key,preview_image_url,type,url" +
      #   "&pagination_token=%s" %next_token)

      #   response = requests.get(url, headers=headers)

      #   if('data' in json.loads(response.text)):
      #     tweets = json.loads(response.text)['data']

      #     medias = []
      #     haveMedias = False

      #     if 'includes' in json.loads(response.text):
      #       if 'media' in json.loads(response.text)['includes']:
      #         medias = json.loads(response.text)['includes']['media']
      #         haveMedias = True

      #     for tweet in tweets:
      #       publicMetrics = tweet['public_metrics']

      #       formattedTweet = {
      #         'text': tweet['text'],
      #         'timestamp': tweet['created_at'],
      #         'quantity_likes': publicMetrics['like_count'],
      #         'quantity_retweets': publicMetrics['retweet_count'],
      #         'quantity_quotes': publicMetrics['quote_count'],
      #         'quantity_replys': publicMetrics['reply_count'],
      #         'twitter_account_id': twitterAccountId,
      #         'url_media': ()
      #       }

      #       if 'attachments' in tweet:
      #         if 'media_keys' in tweet['attachments']:
      #           media_keys = tweet['attachments']['media_keys']

      #           if haveMedias == True:
      #             for media in medias:
      #               for media_key in media_keys:
      #                 if media['media_key'] == media_key and 'preview_image_url' in media:
      #                   formattedTweet['url_media'] += (media['preview_image_url'],)

      #       if len(formattedTweet['url_media']) > 0:
      #         formattedTweet['url_media'] = ','.join(formattedTweet['url_media'])
      #       else:
      #         formattedTweet['url_media'] = ''

      #       await tweetRepository.create(formattedTweet, twitterAccountUsernames[index])

    print("\nTweets inserted successfully into tweets table.\n")
  except HTTPError as http_error:
    print('HTTP error occurred: %s' %http_error)
  except Exception as error:
    print('Internal error occurred: %s' %error)
