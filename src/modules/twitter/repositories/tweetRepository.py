import json

from config import DatabaseConnection

async def create(tweet, username):
  try:
    cursor, connection = await DatabaseConnection.execute()

    getUserIdQuery = """
      SELECT id
      FROM twitter_accounts ta
      WHERE ta.username = '{0}'
    """.format(username)

    cursor.execute(getUserIdQuery)

    twitterAccountId = cursor.fetchone()

    # print(twitterAccountId)
    # print(json.dumps(tweet, indent=4))
    # print('\n')
    
    query = """INSERT INTO tweets (
      text,
      url_media,
      quantity_likes,
      quantity_retweets,
      quantity_quotes,
      quantity_replys,
      timestamp,
      twitter_account_id
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"""

    values = (
      tweet['text'],
      tweet['url_media'],
      tweet['quantity_likes'],
      tweet['quantity_retweets'],
      tweet['quantity_quotes'],
      tweet['quantity_replys'],
      tweet['timestamp'],
      ''.join(twitterAccountId)
    )

    cursor.execute(query, values)

    connection.commit()

    connection.close()
  except Exception as error:
    print('Internal error occurred: %s' %error)