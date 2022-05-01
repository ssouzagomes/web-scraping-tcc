import csv, json

async def create(twitter_accounts, twitter_accounts_writer):
  try:
    for twitter_account in twitter_accounts:
      http_url = 'http://twitter.com/' + twitter_account['username'].lower()
      https_url = 'https://twitter.com/' + twitter_account['username'].lower()
      https_url_www = 'http://www.twitter.com/' + twitter_account['username'].lower()
      http_url_www = 'https://www.twitter.com/' + twitter_account['username'].lower()

      print(twitter_account['username'])

      game_id = None

      csv_file = open('social_networks.csv', 'r')
      csv_reader = csv.DictReader(csv_file)

      for line in csv_reader:
        if (
            line['url'].lower() == http_url or
            line['url'].lower() == https_url or
            line['url'].lower() == https_url_www or
            line['url'].lower() == http_url_www
          ):
          game_id = line['fk_game_id']

      # print(game_id)

      if game_id != None:
        location = ''

        if 'location' in twitter_account:
          location = twitter_account['location']

        values = (
          twitter_account['id'],
          twitter_account['name'],
          twitter_account['username'],
          twitter_account['description'],
          location,
          twitter_account['url'],
          twitter_account['created_at'],
          twitter_account['public_metrics']['following_count'],
          twitter_account['public_metrics']['followers_count'],
          game_id
        )

        # print(json.dumps(values, indent=2))


        twitter_accounts_writer.writerow(values)

    print("\nTwitter accounts inserted successfully into twitter_accounts table.\n")
  except Exception as error:
    print('Internal error occurred: %s' %error)

# async def findById(id):
#   try:
#     cursor, connection = await DatabaseConnection.execute()

#     query = "SELECT twitter_account_id FROM twitter_accounts ta WHERE ta.twitter_account_id = %s"

#     cursor.execute(query, (id,))

#     twitterAccount = cursor.fetchone()

#     connection.close()

#     return ''.join(twitterAccount)
#   except Exception as error:
#     print('Internal error occurred: %s' %error)

