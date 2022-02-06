async def execute(cursor, connection):
  cursor.execute(
    """CREATE TABLE IF NOT EXISTS game (
      id uuid NOT NULL DEFAULT uuid_generate_v4(),
      name character(45) NOT NULL,
      price character(10) NOT NULL,
      release_date timestamp NOT NULL,
      platform character(25),
      description character varying,
      developer character(25),
      publisher character(25),
      genres character varying
    );"""
  )

  cursor.close()

  connection.commit()

  print('Schema created!')