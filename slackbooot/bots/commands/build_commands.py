import websockets
import asyncio
import uuid
import json


class BuildCommand:
    def __init__(self, bot, listen='0.0.0.0', port=8765):
        self.loop = asyncio.get_event_loop()
        self.server = websockets.serve(self.serve, listen, port)
        self.websockets = []
        self.queue = {}
        self.bot = bot
        asyncio.ensure_future(self.server)

    async def enque(self, param, message):
        id = str(uuid.uuid4())
        self.queue[id] = {
            'count': len(self.websockets),
            'param': param,
            'message': message,
        }
        req = json.dumps({'id': id, 'req': param})
        await asyncio.wait([websocket.send(req) for websocket in self.websockets])

    async def serve(self, websocket, path):
        if path != '/build':
            return
        self.websockets.append(websocket)
        try:
            while True:
                resp = await websocket.recv()
                print('received', resp)
                ret = json.loads(resp)
                data = self.queue.get(ret['id'])
                channel = data['message']['channel']
                resp = ret['resp']
                await self.bot.slack.chat.post_message(channel, resp, attachments=[
                    {
                        'title': resp,
                        'fallback': resp,
                        'text': resp
                    }
                ])
                data['count'] -= 1
                if data['count'] <= 0:
                    del self.queue[ret['id']]
        except:
            pass
        finally:
            self.websockets.remove(websocket)
            for k, v in self.queue.items():
                v['count'] -= 1

    async def __call__(self, param, bot, message):
        channel = message['channel']
        keyword = param

        await self.enque(param, message)

        await bot.slack.chat.post_message(channel, 'Builidng {}'.format(keyword), attachments=[
            {
                'title': keyword,
                'fallback': keyword,
                'text': keyword
            }
        ])
