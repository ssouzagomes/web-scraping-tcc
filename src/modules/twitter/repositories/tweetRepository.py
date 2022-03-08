from config import DatabaseConnection

async def create():
  try:
    cursor, connection = await DatabaseConnection.execute()

    query = """INSERT INTO tweets (

    ) VALUES ()"""

    cursor.execute(query)


    formattedUsernames = ','.join(formattedUsernames)

    connection.close()

    return formattedUsernames
  except Exception as error:
    print('Internal error occurred: %s' %error)