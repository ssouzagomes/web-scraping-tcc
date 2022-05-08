import csv

async def create(hardware, minimum_recommended, game_slug, necessary_hardware_writer):
  try:
    csv_file = open('games.csv', 'r')
    csv_reader = csv.DictReader(csv_file)

    game_id = ''

    for row in csv_reader:
      if row['game_slug'] == game_slug:
        game_id = row['id']

    id = game_id + minimum_recommended

    values = (
      id,
      hardware['operacional_system'],
      hardware['processor'],
      hardware['memory'],
      hardware['graphics'],
      hardware['storage'],
      game_id
    )

    necessary_hardware_writer.writerow(values)

  except Exception as error:
    print('Internal error occurred: %s' %error)
