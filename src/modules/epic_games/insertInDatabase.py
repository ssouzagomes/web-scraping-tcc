from config import DatabaseConnection

async def execute(formattedGame, formattedSocialNetworks):
  try:
    insertInGamesQuery = """ INSERT INTO games(
      id,
      name,
      game_slug,
      price,
      release_date,
      platform, description,
      developer,
      publisher,
      genres
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING """

    gameValues = (
      formattedGame['id'],
      formattedGame['name'],
      formattedGame['game_slug'],
      formattedGame['price'],
      formattedGame['release_date'],
      formattedGame['platform'],
      formattedGame['description'],
      formattedGame['developer'],
      formattedGame['publisher'],
      formattedGame['genres']
    )

    cursor, connection = await DatabaseConnection.execute()

    cursor.execute(insertInGamesQuery, gameValues)

    connection.commit()

    insertInSocialNetworkQuery = """ INSERT INTO social_networks(
      description,
      url,
      game_id
    ) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING """

    if len(formattedSocialNetworks) > 0:
      for description in formattedSocialNetworks:
        valuesSocialNetoworks = (
          description,
          formattedSocialNetworks[description],
          formattedGame['id']
        )

        cursor.execute(insertInSocialNetworkQuery, valuesSocialNetoworks)

        connection.commit()

    
  except Exception as error:
    print('Internal error occurred: %s' %error)
