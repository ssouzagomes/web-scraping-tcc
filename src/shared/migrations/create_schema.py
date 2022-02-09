async def execute(cursor, connection):
  cursor.execute(
    """CREATE TABLE IF NOT EXISTS game (
      id uuid NOT NULL DEFAULT uuid_generate_v4(),
      name character varying NOT NULL,
      price character varying NOT NULL,
      release_date timestamp NOT NULL,
      platform character varying,
      description character varying,
      developer character varying,
      publisher character varying,
      genres character varying,
      PRIMARY KEY (id)
    );"""
  )

  cursor.execute(
    """CREATE TABLE IF NOT EXISTS necessary_hardware (
      id uuid NOT NULL DEFAULT uuid_generate_v4(),
      operacional_system character varying NOT NULL,
      processor character varying NOT NULL,
      memory character varying,
      graphics character varying,
      PRIMARY KEY (id)
    );"""
  )

  cursor.execute(
    """ALTER TABLE necessary_hardware
      ADD CONSTRAINT fk_game_id FOREIGN KEY (game_id)
      REFERENCES game(id) ON DELETE CASCADE ON UPDATE CASCADE
    """
  )

  cursor.close()

  connection.commit()

  print('\nSchema created!\n')