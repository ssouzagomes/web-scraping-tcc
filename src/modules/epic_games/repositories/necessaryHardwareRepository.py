async def create(hardware, minimum_recommended, game_id, necessary_hardware_writer):
  try:
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
