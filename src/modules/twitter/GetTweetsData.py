import requests, json, csv
from requests.models import HTTPError

async def execute(user_ids, headers):
  try:
    for user_id in user_ids:
      
      url = ("https://api.twitter.com/2/users/%s/tweets?max_results=5" % user_id +
        "&expansions=attachments.media_keys,in_reply_to_user_id" +
        "&tweet.fields=public_metrics,created_at" +
        "&media.fields=preview_image_url,url")

      response = requests.get(url, headers=headers)

      if('data' in json.loads(response.text)):
        tweets = json.loads(response.text)['data']

        with open(user_id+'-tweets.tsv', 'wt') as out_file:
          for tweet in tweets:
            for column in tweet:
              if(column == 'public_metrics'):
                tsv_writer = csv.writer(out_file, delimiter='\t')
                tsv_writer.writerow(['retweet_count', tweet[column]['retweet_count']])

                tsv_writer = csv.writer(out_file, delimiter='\t')
                tsv_writer.writerow(['reply_count', tweet[column]['reply_count']])

                tsv_writer = csv.writer(out_file, delimiter='\t')
                tsv_writer.writerow(['like_count', tweet[column]['like_count']])

                tsv_writer = csv.writer(out_file, delimiter='\t')
                tsv_writer.writerow(['quote_count', tweet[column]['quote_count']])
              
              else:
                tsv_writer = csv.writer(out_file, delimiter='\t')
                tsv_writer.writerow([column, tweet[column]])


  except HTTPError as http_error:
    print('HTTP error occurred: %s' %http_error)
  except Exception as error:
    print('Internal error occurred: %s' %error)