import asyncio
import websockets
import json


async def ping(websocket):
    while True:
        await websocket.ping()
        print('ping')
        await asyncio.sleep(30)


async def hello():
    '''
    <<< {"raw": {"text": "build", "team": "T03HJ5ZNK", "user": "U0FMC5K53", "channel": "D0H28224C", "ts": "1451997825.000058", "type": "message"}, "req": ""}
    >>> {"raw": {"type": "message", "ts": "1451997825.000058", "user": "U0FMC5K53", "team": "T03HJ5ZNK", "text": "build", "channel": "D0H28224C"}, "req": "", "resp": {"title": "Build completed!", "text": "Cccc"}}
    '''
    websocket = await websockets.connect('ws://slackbooot.herokuapp.com/build')
    asyncio.ensure_future(ping(websocket))

    while True:
        s = await websocket.recv()
        print("<<< {}".format(s))
        greeting = json.loads(s)
        greeting['resp'] = {
            'title': 'Build completed!',
            'text': 'Cccc',
        }
        resp = json.dumps(greeting)
        await websocket.send(resp)
        print(">>> {}".format(resp))


loop = asyncio.get_event_loop()
loop.run_until_complete(hello())
