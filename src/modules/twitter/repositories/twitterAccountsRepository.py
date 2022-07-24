import csv

async def create(twitter_accounts, twitter_accounts_writer):
  try:
    for twitter_account in twitter_accounts:
      http_url = 'http://twitter.com/' + twitter_account['username'].lower()
      https_url = 'https://twitter.com/' + twitter_account['username'].lower()
      https_url_www = 'http://www.twitter.com/' + twitter_account['username'].lower()
      http_url_www = 'https://www.twitter.com/' + twitter_account['username'].lower()

      game_id = None

      csv_file = open('social_networks.csv', 'r')
      csv_reader = csv.DictReader(csv_file)

      for row in csv_reader:
        if (
            row['url'].lower() == http_url or
            row['url'].lower() == https_url or
            row['url'].lower() == https_url_www or
            row['url'].lower() == http_url_www
          ):
          game_id = row['fk_game_id']

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

        twitter_accounts_writer.writerow(values)

      csv_file.close()

    print("\nTwitter accounts saved successfully into twitter_accounts.csv file.\n")
  except Exception as error:
    print('Internal error occurred: %s' %error)

async def findById(id):
  try:
    csv_file = open('twitter_accounts.csv', 'r')
    csv_reader = csv.DictReader(csv_file)

    twitterAccount = ''

    for row in csv_reader:
      if row['id'] == id:
        print(row['id'])

    csv_file.close()

  except Exception as error:
    print('Internal error occurred: %s' %error)
