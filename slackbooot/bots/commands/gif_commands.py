import aiohttp


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
