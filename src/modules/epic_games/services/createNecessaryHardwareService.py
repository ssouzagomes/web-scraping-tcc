from modules.epic_games.repositories import necessaryHardwareRepository

async def execute(addicional_game_infos, game_ids, necessary_hardware_writer):
  try:
    for index, addicional_game_info in enumerate(addicional_game_infos):
      if 'requirements' in addicional_game_info:
        if 'systems' in addicional_game_info['requirements']:
          if 'details' in addicional_game_info['requirements']['systems'][0]:
            game_id = game_ids[index]
            
            specifications = addicional_game_info['requirements']['systems'][0]['details']

            operacional_system_minimum = ''
            processor_minimum = ''
            memory_minimum = ''
            graphics_minimum = ''
            storage_minimum = ''

            operacional_system_recommended = ''
            processor_recommended = ''
            memory_recommended = ''
            graphics_recommended = ''
            storage_recommended = ''

            hasMinimum = False
            hasRecommended = False

            for specification in specifications:
              if 'minimum' in specification:
                hasMinimum = True
                if specification['title'] == 'OS':
                  operacional_system_minimum = specification['minimum']
                if specification['title'] == 'Processor' or specification['title'] == 'CPU':
                  processor_minimum = specification['minimum']
                if specification['title'] == 'Memory' or specification['title'] == 'RAM':
                  memory_minimum = specification['minimum']
                if specification['title'] == 'Graphics' or specification['title'] == 'GPU' or specification['title'] == 'Video':
                  graphics_minimum = specification['minimum']
                if specification['title'] == 'Storage' or specification['title'] == 'HDD':
                  storage_minimum = specification['minimum']

            for specification in specifications:
              if 'recommended' in specification:
                hasRecommended = True
                if specification['title'] == 'OS':
                  operacional_system_recommended = specification['recommended']
                if specification['title'] == 'Processor' or specification['title'] == 'CPU':
                  processor_recommended = specification['recommended']
                if specification['title'] == 'Memory' or specification['title'] == 'RAM':
                  memory_recommended = specification['recommended']
                if specification['title'] == 'Graphics' or specification['title'] == 'GPU' or specification['title'] == 'Video':
                  graphics_recommended = specification['recommended']
                if specification['title'] == 'Storage' or specification['title'] == 'HDD':
                  storage_recommended = specification['recommended']

            if hasMinimum:
              minimum_formatted = {
                'operacional_system': operacional_system_minimum,
                'processor': processor_minimum,
                'memory': memory_minimum,
                'graphics': graphics_minimum,
                'storage': storage_minimum
              }

              minimum = '1'

              await necessaryHardwareRepository.create(minimum_formatted, minimum, game_id, necessary_hardware_writer)

            if hasRecommended:
              recommended_formatted = {
                'operacional_system': operacional_system_recommended,
                'processor': processor_recommended,
                'memory': memory_recommended,
                'graphics': graphics_recommended,
                'storage': storage_recommended
              }

              recommended = '2'

              await necessaryHardwareRepository.create(recommended_formatted, recommended, game_id, necessary_hardware_writer)
              
          print("Necessary hardware saved successfully into necessary_hardware.csv file.\n")


  except Exception as error:
    print('Internal error occurred: %s' % error)
