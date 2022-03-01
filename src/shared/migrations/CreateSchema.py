async def execute(cursor, connection):
  cursor.execute(
    """CREATE TABLE IF NOT EXISTS games (
      id INT UNIQUE NOT NULL,
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
    """CREATE TABLE IF NOT EXISTS specifications (
      id uuid NOT NULL DEFAULT uuid_generate_v4(),
      operacional_system character varying NOT NULL,
      processor character varying NOT NULL,
      memory character varying,
      graphics character varying,
      storage character varying,
      languages character varying,
      game_id INT NOT NULL,
      PRIMARY KEY (id),
      FOREIGN KEY (game_id) REFERENCES games (id)
    );"""
  )

  cursor.execute(
    """CREATE TABLE IF NOT EXISTS critic (
      id uuid NOT NULL DEFAULT uuid_generate_v4(),
      company character varying,
      author character varying NOT NULL,
      rating character varying NOT NULL,
      comment character varying NOT NULL,
      date timestamp NOT NULL,
      top_critic BOOLEAN NOT NULL DEFAULT FALSE,
      game_id INT NOT NULL,
      PRIMARY KEY (id),
      FOREIGN KEY (game_id) REFERENCES games (id)
    );"""
  )

  cursor.execute(
    """CREATE TABLE IF NOT EXISTS twitter_accounts (
      id uuid NOT NULL DEFAULT uuid_generate_v4(),
      name character varying NOT NULL,
      username character varying NOT NULL,
      bio character varying,
      location character varying,
      website character varying,
      join_date timestamp NOT NULL,
      following INT NOT NULL,
      followers INT NOT NULL,
      game_id INT NOT NULL,
      PRIMARY KEY (id),
      FOREIGN KEY (game_id) REFERENCES games (id)
    );"""
  )

  cursor.execute(
    """CREATE TABLE IF NOT EXISTS tweets (
      id uuid NOT NULL DEFAULT uuid_generate_v4(),
      text character varying NOT NULL,
      url_media character varying,
      quantity_likes INT,
      quantity_retweets INT,
      quantity_quotes INT,
      quantity_comments INT,
      timestamp timestamp NOT NULL,
      twitter_account_id uuid NOT NULL,
      PRIMARY KEY (id),
      FOREIGN KEY (twitter_account_id) REFERENCES twitter_accounts (id)
    );"""
  )

  cursor.execute(
    """CREATE TABLE IF NOT EXISTS social_networks (
      id uuid NOT NULL DEFAULT uuid_generate_v4(),
      description character varying NOT NULL,
      url character varying NOT NULL,
      game_id INT NOT NULL,
      PRIMARY KEY (id),
      FOREIGN KEY (game_id) REFERENCES games (id)
    );"""
  )

  cursor.close()

  connection.commit()

  print('\nSchema created!\n')