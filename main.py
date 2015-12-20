import aiohttp
import asyncio
import operator
import os
import re

import butterfield
from butterfield import Bot

TOKEN = os.environ.get('TOKEN')


class CommandBot(Bot):

    def __init__(self, *args, **kwargs):
        super(CommandBot, self).__init__(*args, **kwargs)
        self.listen(self.message_handler)
        self.command_handlers = []

    async def message_handler(self, bot, message: 'message'):
        if 'subtype' in message:
            return

        text = message['text']

        for commands, coro in self.command_handlers:
            regexp = r'^\s*%s\s*' % (r'\s*'.join(commands))
            pattern = re.compile(regexp)
            match = pattern.match(text)
            if not match:
                continue
            prefix = match.group(0)

            param = text[len(prefix):].strip()

            return asyncio.ensure_future(coro(param, bot, message))

    def listen_on_command(self, commands, coro):
        self.command_handlers.append((commands, coro))
        self.command_handlers.sort(key=operator.itemgetter(0), reverse=True)


async def search_gif(q):
    url = 'http://api.giphy.com/v1/gifs/translate'
    params = {'api_key': 'dc6zaTOxFJmzC', 's': q}
    resp = await aiohttp.get(url, params=params)
    ret = await resp.json()
    if not ret or not ret['data']:
        return ''
    return ret['data']


async def find_gif(param, bot, message):
    channel = message['channel']
    keyword = param
    gif_content = await search_gif(keyword)
    if not gif_content:
        await bot.post(channel, 'No gif about "%s" found' % keyword)
        return

    await bot.slack.chat.post_message(channel, keyword, attachments=[
        {
            'image_url': gif_content['images']['fixed_width']['url'],
            'title': keyword,
            'title_link': gif_content['url'],
        }
    ])


async def gif_trends(param, bot, message):
    channel = message['channel']
    resp = await aiohttp.get('http://api.giphy.com/v1/gifs/trending?api_key=dc6zaTOxFJmzC&limit=%s' % param)
    content = await resp.json()
    attachments = [
        {
            'image_url': gif['images']['fixed_width']['url'],
            'title': "Gif Trending %d" % (i+1),
            'title_link': gif['url'],
        } for i, gif in enumerate(content['data'])
    ]

    await bot.slack.chat.post_message(channel, 'Gif Trending', attachments=attachments)


async def bilibili_treding(bot, message: 'message'):
    if 'subtype' in message:
        return

    channel = message['channel']
    text = message['text']
    if not text.startswith('gif'):
        return
    keyword = text[4:].strip()
    gif_content = await search_gif(keyword)
    if not gif_content:
        await bot.post(channel, 'No gif about "%s" found' % keyword)
        return

    await bot.slack.chat.post_message(channel, keyword, attachments=[
        {
            'image_url': gif_content['images']['fixed_width']['url'],
            'title': keyword,
            'title_link': gif_content['url'],
        }
    ])


b = CommandBot(TOKEN)
b.listen_on_command(['gif'], find_gif)
b.listen_on_command(['gif', 'trends'], gif_trends)

butterfield.run(b)
