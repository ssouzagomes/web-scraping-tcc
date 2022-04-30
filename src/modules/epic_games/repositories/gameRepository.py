import csv
import json

async def create(formattedGames):
  try:
    games = formattedGames

    data_file = open('games.csv', 'w')
    
    csv_writer = csv.writer(data_file)
    
    count = 0
    
    for game in games:
      if count == 0:
  
        header = game.keys()
        csv_writer.writerow(header)
        count += 1
  
      values = game.values()
      csv_writer.writerow(values)
    
    data_file.close()

    print("\nGames saved successfully into games.csv file.")
  except Exception as error:
    print('Internal error occurred: %s' %error)
