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

    for row in csv_reader:
      if row['description'] == 'linkTwitter':
        usernames.append(row['url'])

    for username in usernames:
      username = ''.join(username)
      username = username.replace('https://twitter.com/', '')
      username = username.replace('http://twitter.com/', '')
      username = username.replace('https://www.twitter.com/', '')
      username = username.replace('http://www.twitter.com/', '')
      
      index = -1

      if '/' in username:
        index = username.index('/')

      if index > -1:
        username = username[:index]

      username = username.replace('https:', '')
      username = username.replace('http:', '')
      username = username.replace('.comtwitter', '')
      username = username.replace(' ', '') 

      index = -1

      if '?' in username:
        index = username.index('?')

      if index > -1:
        username = username[:index-1]

      if username != '':
        formattedUsernames.append(username)

    csv_file.close()

    return formattedUsernames
  except Exception as error:
    print('Internal error occurred: %s' %error)
