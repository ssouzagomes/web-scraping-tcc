from config import DatabaseConnection

async def create(twitter_accounts):
  try:
    cursor, connection = await DatabaseConnection.execute()

    queryTwitterAccount = '''INSERT INTO twitter_accounts (
      name,
      username,
      bio,
      location,
      website,
      join_date,
      following,
      followers,
      game_id,
      twitter_account_id
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING'''

    for twitter_account in twitter_accounts:
      http_url = 'http://twitter.com/' + twitter_account['username']
      https_url = 'https://twitter.com/' + twitter_account['username']

      queryGameId = '''
        SELECT game_id
        FROM social_networks sn
        WHERE sn.url = %s or sn.url = %s
      '''

      valuesGameId = (http_url, https_url)

      cursor.execute(queryGameId, valuesGameId)

      game_id = cursor.fetchone()

      if game_id != None:
        game_id = ''.join(game_id)

        location = ''
        if 'location' in twitter_account:
          location = twitter_account['location']

        valuesTwitterAccount = (
          twitter_account['name'],
          twitter_account['username'],
          twitter_account['description'],
          location,
          twitter_account['url'],
          twitter_account['created_at'],
          twitter_account['public_metrics']['following_count'],
          twitter_account['public_metrics']['followers_count'],
          game_id,
          twitter_account['id']
        )

        cursor.execute(queryTwitterAccount, valuesTwitterAccount)

        connection.commit()

    connection.close()

    print("\nTwitter accounts inserted successfully into twitter_accounts table.\n")
  except Exception as error:
    print('Internal error occurred: %s' %error)

async def findById(id):
  try:
    cursor, connection = await DatabaseConnection.execute()

    query = "SELECT twitter_account_id FROM twitter_accounts ta WHERE ta.twitter_account_id = %s"

    cursor.execute(query, (id,))

    twitterAccount = cursor.fetchone()

    connection.close()

    return ''.join(twitterAccount)
  except Exception as error:
    print('Internal error occurred: %s' %error)

