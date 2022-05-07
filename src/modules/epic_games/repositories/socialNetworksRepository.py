import csv

async def create(socialNetworks):
  try:
    data_file = open('social_networks.csv', 'w')
        
    csv_writer = csv.writer(data_file)
    
    count = 0

    for socialNetwork in socialNetworks:
      if count == 0:

        header = socialNetwork.keys()
        csv_writer.writerow(header)
        count += 1
  
      values = socialNetwork.values()
      csv_writer.writerow(values)
    
    data_file.close()
    
    print("Social networks saved successfully into social_networks.csv file.")

  except Exception as error:
    print('Internal error occurred: %s' %error)

async def getAllUsernames():
  try:
    csv_file = open('social_networks.csv', 'r')
    csv_reader = csv.DictReader(csv_file)

    formattedUsernames = []
    usernames = []

    for line in csv_reader:
      if line['description'] == 'linkTwitter':
        usernames.append(line['url'])

    for username in usernames:
      username = ''.join(username)
      username = username.replace('https://twitter.com/', '')
      username = username.replace('http://twitter.com/', '')
      username = username.replace('https://www.twitter.com/', '')
      username = username.replace('http://www.twitter.com/', '')
      username = username.replace('?lang=en', '')
      username = username.replace('/', '')
      username = username.replace('https:', '')
      username = username.replace('http:', '')
      username = username.replace('.comtwitter', '')
      username = username.replace(' ', '')
      formattedUsernames.append(username)

    csv_file.close()

    return formattedUsernames
  except Exception as error:
    print('Internal error occurred: %s' %error)
