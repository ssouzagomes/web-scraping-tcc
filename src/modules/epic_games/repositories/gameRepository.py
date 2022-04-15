from config import DatabaseConnection

async def create(formattedGame):
  try:
    query = '''INSERT INTO games(
      id,
      name,
      game_slug,
      price,
      release_date,
      platform,
      description,
      developer,
      publisher,
      genres
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING'''

    values = (
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

    cursor.execute(query, values)

    connection.commit()

    print("\nGame inserted successfully into games table.")
  except Exception as error:
    print('Internal error occurred: %s' %error)