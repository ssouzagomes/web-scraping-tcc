async def create(formattedGames, games_writer):
  try:
    games = formattedGames

    for game in games:
      values = (
        game['id'],
        game['name'],
        game['game_slug'],
        game['price'],
        game['release_date'],
        game['platform'],
        game['description'],
        game['developer'],
        game['publisher'],
        game['genres']
      )
     
      games_writer.writerow(values)
    
    print("\nGames saved successfully into games.csv file.")
  except Exception as error:
    print('Internal error occurred: %s' %error)
