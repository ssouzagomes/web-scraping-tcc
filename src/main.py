import asyncio

from config.twitter_authenticate import headers
from modules.twitter import get_user_data

asyncio.run(get_user_data.__main__(headers))
