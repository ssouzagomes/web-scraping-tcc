async def create(tweet, tweets_writer):
  try:
    values = (
      tweet['id'],
      tweet['text'],
      tweet['url_media'],
      tweet['quantity_likes'],
      tweet['quantity_retweets'],
      tweet['quantity_quotes'],
      tweet['quantity_replys'],
      tweet['timestamp'],
      tweet['in_reply_to_user_id'],
      tweet['twitter_account_id']
    )

    tweets_writer.writerow(values)

  except Exception as error:
    print('Internal error occurred: %s' %error)