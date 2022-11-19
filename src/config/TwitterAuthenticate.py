from requests.structures import CaseInsensitiveDict
from configparser import ConfigParser

config = ConfigParser(interpolation=None)
config.read('env.ini')

twitter_api = config['twitter_api']

API_KEY = twitter_api['api_key']
API_KEY_SECRET = twitter_api['api_key_secret']
BEARER_TOKEN = twitter_api['bearer_token']
ACCESS_TOKEN = twitter_api['access_token']
ACCESS_TOKEN_SECRET = ['access_token_secret']

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Authorization"] = "Bearer " + BEARER_TOKEN

baseUrl = twitter_api['url']