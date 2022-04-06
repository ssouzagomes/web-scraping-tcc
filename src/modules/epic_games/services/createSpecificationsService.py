async def execute(addicional_game_info):
  try:
    specifications = addicional_game_info['requirements']['systems']

    file = open("specifications.json","w")
    file.write(specifications)
    file.close()
  except Exception as error:
    print('Internal error occurred: %s' % error)