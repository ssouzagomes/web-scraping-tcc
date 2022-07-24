import requests, json, csv
from requests.models import HTTPError

from modules.open_critic.repositories import gameReviewRepository

async def execute():
  try:
    open_critic_file = open('open_critic.csv', 'w')
    open_critic_writer = csv.writer(open_critic_file)
    header_open_critic_file = (
      'id', 'company', 'author', 'rating', 'comment', 'date', 'top_critic', 'game_id'
    )
    open_critic_writer.writerow(header_open_critic_file)

    response = requests.get("https://api.opencritic.com/api/game")

    games = json.loads(response.text)

    formattedGames = []

    for game in games:
      formattedGame = {
        'id': game['id'],
        'name': game['name']
      }

      formattedGames.append(formattedGame)

    skip = 20

    while len(games) > 0:
      response = requests.get("https://api.opencritic.com/api/game?skip={}".format(skip))

      games = json.loads(response.text)

      for game in games:
        formattedGame = {
          'id': game['id'],
          'name': game['name']
        }

        formattedGames.append(formattedGame)

      skip += 20

    for formatted_game in formattedGames:
      epic_games_id = await gameReviewRepository.findGame(formatted_game)

      open_critc_game_id = formatted_game['id']

      if epic_games_id != None:
        print('\nGet open critic game.\n')
        responseReview = requests.get("https://api.opencritic.com/api/review/game/{}?sort=date&order=desc".format(open_critc_game_id))

        reviews = json.loads(responseReview.text)

        for review in reviews:
          authors = []

          for author in review['Authors']:
            authors.append(author['name'])

          score = ''
          snippet = ''

          if 'score' in review:
            score = review['score']
          if 'snippet' in review:
            snippet = review['snippet']

          formattedReview = (
            review['_id'],
            review['Outlet']['name'],
            ','.join(authors),
            score,
            snippet,
            review['publishedDate'],
            not review['Outlet']['isContributor'],
            epic_games_id
          )

          await gameReviewRepository.create(formattedReview, open_critic_writer)

        skipReview = 20

        while len(reviews) > 0:
          responseReview = requests.get("https://api.opencritic.com/api/review/game/{}?sort=date&order=desc&skip={}".format(open_critc_game_id, skipReview))

          reviews = json.loads(responseReview.text)

          for review in reviews:
            authors = []

            for author in review['Authors']:
              authors.append(author['name'])

            score = ''
            snippet = ''

            if 'score' in review:
              score = review['score']
            if 'snippet' in review:
              snippet = review['snippet']

            formattedReview = (
              review['_id'],
              review['Outlet']['name'],
              ','.join(authors),
              score,
              snippet,
              review['publishedDate'],
              not review['Outlet']['isContributor'],
              epic_games_id
            )

            await gameReviewRepository.create(formattedReview, open_critic_writer)

            skipReview += 20

          print('Game reviews saved successfully in open_critic.csv file')

    open_critic_file.close()

  except HTTPError as http_error:
    print('HTTP error occurred: %s' %http_error)
  except Exception as error:
    print('Internal error occurred: %s' %error)
