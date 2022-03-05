import asyncio

from config import DatabaseConnection

async def getAllUsernames():
  try:
    cursor, connection = await DatabaseConnection.execute()

    query = "SELECT url FROM social_networks sn WHERE sn.description = 'linkTwitter'"

    cursor.execute(query)

    usernames = cursor.fetchall()

    formattedUsernames = []

    for username in usernames:
      username = ''.join(username)
      username = username.replace('https://twitter.com/', '')
      username = username.replace('http://twitter.com/', '')
      username = username.replace('/', '')
      formattedUsernames.append(username)

    formattedUsernames = ','.join(formattedUsernames)

    connection.close()

    return formattedUsernames
  except Exception as error:
    print('Internal error occurred: %s' %error)