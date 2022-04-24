import psycopg2

from config import DatabaseConnection

async def create(hardware, minimum_recommended, game_slug):
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
      id,
      operacional_system,
      processor,
      memory,
      graphics,
      storage,
      game_id
    ) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING'''

    game_id = ''.join(game_id)

    hardware_id = game_id + minimum_recommended

    values = (
      hardware_id,
      hardware['operacional_system'],
      hardware['processor'],
      hardware['memory'],
      hardware['graphics'],
      hardware['storage'],
      game_id
    )

    cursor.execute(query, values)

    connection.commit()  
  except (Exception, psycopg2.Error) as error:
    print("Error while fetching data from PostgreSQL", error)

  finally:
    if connection:
      cursor.close()
      connection.close()
