from requests.models import HTTPError

from modules.epic_games.repositories import socialNetworksRepository

async def execute(formattedGame, addicionalGameInfo):
  try:
    socialNetworks = addicionalGameInfo['socialLinks']

    if '_type' in socialNetworks:
      del socialNetworks['_type']
    if 'title' in socialNetworks:
      del socialNetworks['title']
    if 'linkHomepage' in socialNetworks:
      del socialNetworks['linkHomepage']

    formattedSocialNetworks = {}

    for key in socialNetworks:
      if socialNetworks[key] != '':
        formattedSocialNetworks[key] = socialNetworks[key]

    # specifications = addicionalGameInfo['requirements']['systems']

    # print(json.dumps(specifications, indent=4))

    # formattedSpecifications = []

    # for specification in specifications:
    #   if '_type' in specification:
    #     del specification['_type']
    #   formattedSpecifications.append(specification)

    # print(json.dumps(formattedSpecifications, indent=4))

    await socialNetworksRepository.create(formattedGame, formattedSocialNetworks)

  except HTTPError as http_error:
    print('HTTP error occurred: %s' % http_error)
  except Exception as error:
    print('Internal error occurred: %s' % error)
