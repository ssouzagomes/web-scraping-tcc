import asyncio

from config.twitter_authenticate import headers
from modules.twitter import get_users_data

asyncio.run(get_users_data.execute(headers))
