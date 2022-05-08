import csv

async def create(formatted_review, open_critic_writer):
  try:
    open_critic_writer.writerow(formatted_review)

  except Exception as error:
    print('Internal error occurred: %s' %error)

async def findGame(formatted_game):
  try:
    csv_file = open('games.csv')
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
      if formatted_game['name'] in row['name']:
        return row['id']

  except Exception as error:
    print('Internal error occurred: %s' %error)
