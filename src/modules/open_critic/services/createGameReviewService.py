import requests, json
from requests.models import HTTPError

async def execute():
  try:
    
    # response = requests.get("https://api.opencritic.com/api/review/game/163")
    response = requests.get("https://api.opencritic.com/api/review/game/163?sort=date&order=desc")

    critic =json.loads(response.text)[0]

    print(json.dumps(critic, indent = 2))

    file = open("open-critic.json","w")
    file.write(response.text)
    file.close()
          
  except HTTPError as http_error:
    print('HTTP error occurred: %s' %http_error)
  except Exception as error:
    print('Internal error occurred: %s' %error)
