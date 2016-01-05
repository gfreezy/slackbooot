import websockets
import asyncio
import json


class BuildCommand:
    def __init__(self, bot, listen='0.0.0.0', port=8765):
        self.loop = asyncio.get_event_loop()
        self.server = websockets.serve(self.serve, listen, port)
        self.websockets = []
        self.bot = bot
        asyncio.ensure_future(self.server)

    async def serve(self, websocket, path):
        if path != '/build':
            return
        self.websockets.append(websocket)
        print('New websocket connected[{}]'.format(len(self.websockets)))
        try:
            while True:
                resp = await websocket.recv()
                print('received', resp)
                ret = json.loads(resp)

                try:
                    channel = ret['raw']['channel']
                except:
                    await websocket.send(json.dumps({'status': 'error', 'message': 'Missing "raw"'}))
                    continue

                resp = ret.get('resp', {})
                title = resp.get('title', '')
                text = resp.get('text', '')

                await self.bot.slack.chat.post_message(channel, '', attachments=[
                    {
                        'title': title,
                        'text': text,
                        'fallback': title,
                    }
                ])
        except websockets.exceptions.ConnectionClosed:
            pass

        finally:
            self.websockets.remove(websocket)
            print('Websocket disconnected[{}]'.format(len(self.websockets)))

    async def __call__(self, param, bot, message):
        channel = message['channel']
        keyword = param

        req = json.dumps({'req': param, 'raw': message})

        msg = ('Build failed!', 'No worker connected!!!')
        if self.websockets:
            msg = ('Building {}'.format(keyword), 'Work work hard!!!')
            asyncio.ensure_future(asyncio.wait([websocket.send(req) for websocket in self.websockets], timeout=10))

        await bot.slack.chat.post_message(channel, '', attachments=[
            {
                'title': msg[0],
                'text': msg[1],
                'fallback': msg[0],
            }
        ])
