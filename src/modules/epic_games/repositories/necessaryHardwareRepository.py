import psycopg2

from config import DatabaseConnection

async def create(minimum_formatted, recommended_formatted, game_slug):
  try:

    cursor, connection = await DatabaseConnection.execute()

    queryGameId = '''
        SELECT id
        FROM games g
        WHERE g.game_slug = %s
    '''

    cursor.execute(queryGameId, (game_slug,))

    game_id = cursor.fetchone()

    query = '''INSERT INTO necessary_hardware(
      operacional_system,
      processor,
      memory,
      graphics,
      storage,
      game_id
    ) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING'''

    values = (
      minimum_formatted['operacional_system'],
      minimum_formatted['processor'],
      minimum_formatted['memory'],
      minimum_formatted['graphics'],
      minimum_formatted['storage'],
      game_id
    )

    cursor.execute(query, values)

    connection.commit()

    print("Necessary hardware inserted successfully into necessary_hardware table.\n")
  
  except (Exception, psycopg2.Error) as error:
    print("Error while fetching data from PostgreSQL", error)

  finally:
    if connection:
      cursor.close()
      connection.close()
