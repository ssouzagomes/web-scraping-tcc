from requests.models import HTTPError

from modules.epic_games.repositories import socialNetworksRepository

async def execute(addicionalGameInfos):
  try:
    formattedSocialNetworks = []

    for addicionalGameInfo in addicionalGameInfos:
      socialNetworks = addicionalGameInfo['socialNetworks']
      gameId = addicionalGameInfo['gameId']

      if '_type' in socialNetworks:
        del socialNetworks['_type']
      if 'title' in socialNetworks:
        del socialNetworks['title']
      if 'linkHomepage' in socialNetworks:
        del socialNetworks['linkHomepage']

      formattedSocialNetwork = {
        'fk_game_id': gameId
      }

      for key in socialNetworks:
        if socialNetworks[key] != '':
          formattedSocialNetwork[key] = socialNetworks[key]

      if len(formattedSocialNetwork) > 1:
        formattedSocialNetworks.append(formattedSocialNetwork)   

    socialNetworks = []

    id = 1000
    
    if len(formattedSocialNetworks) > 0:
      for socialNetwork in formattedSocialNetworks:
        for key in socialNetwork:

          url = ''
          fk_game_id = ''
          description = ''
          
          if key != 'fk_game_id':
            description = key
            url = socialNetwork[key]
            fk_game_id = socialNetwork['fk_game_id']


          formattedSocialNetwork = {
            'id': id,
            'description': description,
            'url': url,
            'fk_game_id': fk_game_id
          }

          id += 1

          if formattedSocialNetwork['fk_game_id'] != '':
            socialNetworks.append(formattedSocialNetwork)

    await socialNetworksRepository.create(socialNetworks)
    
  except HTTPError as http_error:
    print('HTTP error occurred: %s' % http_error)
  except Exception as error:
    print('Internal error occurred: %s' % error)
