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
      game_id
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING'''

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

      valuesTwitterAccount = (
        twitter_account['name'],
        twitter_account['username'],
        twitter_account['description'],
        twitter_account['location'],
        twitter_account['url'],
        twitter_account['created_at'],
        twitter_account['public_metrics']['following_count'],
        twitter_account['public_metrics']['followers_count'],
        ''.join(game_id)
      )

      cursor.execute(queryTwitterAccount, valuesTwitterAccount)

      connection.commit()

    connection.close()

    print("\nRecord inserted successfully into games table.\n")
  except Exception as error:
    print('Internal error occurred: %s' %error)