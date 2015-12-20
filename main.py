import aiohttp
import random
import os

import butterfield
from butterfield import Bot


TOKEN = os.environ.get('TOKEN')


async def search_gif(q):
    url = 'http://api.giphy.com/v1/gifs/search'
    params = {'api_key': 'dc6zaTOxFJmzC', 'q': q}
    resp = await aiohttp.get(url, params=params)
    ret = await resp.json()
    if not ret or not ret['data']:
        return ''
    first = random.choice(ret['data'])
    return first['images']['fixed_width']['url']


async def find_gif(bot, message: 'message'):
    if 'subtype' in message:
        return

    channel = message['channel']
    text = message['text']
    if not text.startswith('gif'):
        return
    keyword = text[4:].strip()
    gif = await search_gif(keyword)
    if not gif:
        await bot.post(channel, 'No gif about "%s" found' % keyword)
        return
    await bot.post(channel, gif)


b = Bot(TOKEN)
b.listen(find_gif)

butterfield.run(b)
