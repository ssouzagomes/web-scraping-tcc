import requests, json, csv
from requests.models import HTTPError

# async def execute():
try:
  response = requests.get("https://api.opencritic.com/api/review/game/163")

  print(len(json.loads(response.text)))

  # games = json.loads(response.text)['data']['Catalog']['searchStore']['elements']

  # with open('games.csv', 'wt') as out_file:
  #   for game in games:
  #     for column in game:
  #       tsv_writer = csv.writer(out_file, delimiter='\t')
  #       tsv_writer.writerow([column, game[column]])
        
except HTTPError as http_error:
  print('HTTP error occurred: %s' %http_error)
except Exception as error:
  print('Internal error occurred: %s' %error)